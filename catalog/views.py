"""
Контроллеры приложения catalog (CBV).

- HomeView: главная страница — список товаров (ListView), с пагинацией
  и печатью в консоль 5 последних добавленных продуктов. Единственная
  страница товаров, доступная без входа.
- ProductDetailView: подробная страница товара (DetailView).
- ProductCreateView / ProductUpdateView / ProductDeleteView: создание,
  редактирование и удаление товара. Доступны только вошедшим
  пользователям (LoginRequiredMixin, урок 7).
- ContactsView: страница контактов с данными из модели ContactInfo и
  обработкой формы обратной связи (View — отдельные get()/post()).

Права (урок 8):
- при создании владельцем товара (owner) становится текущий пользователь;
- редактировать товар целиком может только владелец;
- модератор (право can_unpublish_product) может открыть форму
  редактирования, но в ней только статус публикации, и снять его можно
  лишь в сторону «не опубликован»;
- удалить товар может владелец или модератор (право delete_product);
- неопубликованные товары видят только их владелец и модераторы.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import ContactInfo, Product

PRODUCTS_PER_PAGE = 6

UNPUBLISH_PERMISSION = "catalog.can_unpublish_product"
DELETE_PERMISSION = "catalog.delete_product"


def visible_products(user):
    """Товары, которые пользователь может видеть.

    Гость — только опубликованные; вошедший пользователь — опубликованные
    и свои; модератор — все.
    """
    products = Product.objects.select_related("category", "owner")
    if user.has_perm(UNPUBLISH_PERMISSION):
        return products
    if user.is_authenticated:
        return products.filter(Q(is_published=True) | Q(owner=user))
    return products.filter(is_published=True)


def is_owner(user, product):
    return user.is_authenticated and product.owner_id == user.pk


class HomeView(ListView):
    """Главная страница — список товаров с пагинацией."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = PRODUCTS_PER_PAGE

    def get_queryset(self):
        latest_products = Product.objects.select_related("category").order_by("-created_at")[:5]

        print("Последние 5 добавленных продуктов:")
        for product in latest_products:
            print(f"  [{product.id}] {product.name} — {product.price} ({product.category.name})")

        return visible_products(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная"
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Страница с подробной информацией о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return visible_products(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Форма добавления нового товара; владелец — текущий пользователь."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить товар"
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара: владелец — полная форма, модератор — только статус."""

    model = Product
    template_name = "catalog/product_form.html"

    def get_queryset(self):
        return visible_products(self.request.user)

    def get_form_class(self):
        user = self.request.user
        if is_owner(user, self.object):
            return ProductForm
        if user.has_perm(UNPUBLISH_PERMISSION):
            return ProductModeratorForm
        raise PermissionDenied("Редактировать товар может только его владелец или модератор.")

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if is_owner(self.request.user, self.object):
            context["title"] = "Редактировать товар"
        else:
            context["title"] = "Модерация товара"
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара владельцем или модератором; после удаления — на главную."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

    def get_queryset(self):
        return visible_products(self.request.user)

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        user = self.request.user
        if not is_owner(user, product) and not user.has_perm(DELETE_PERMISSION):
            raise PermissionDenied("Удалить товар может только его владелец или модератор.")
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление товара"
        return context


class ContactsView(View):
    """Страница контактов + обработка формы обратной связи."""

    template_name = "catalog/contacts.html"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Контакты",
            "success": False,
            "contact_info": ContactInfo.objects.first(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        print("Получены данные формы обратной связи:")
        print(f"  Имя: {name}")
        print(f"  Почта: {email}")
        print(f"  Сообщение: {message}")

        context = {
            "title": "Контакты",
            "success": True,
            "name": name,
            "contact_info": ContactInfo.objects.first(),
        }
        return render(request, self.template_name, context)
