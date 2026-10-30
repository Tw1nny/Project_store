"""
Контроллеры приложения catalog (CBV).

- HomeView: главная страница — список товаров (ListView), с пагинацией
  и печатью в консоль 5 последних добавленных продуктов.
- ProductDetailView: подробная страница товара (DetailView).
- ProductCreateView / ProductUpdateView / ProductDeleteView: создание,
  редактирование и удаление товара (CRUD, урок 6). Создание
  и редактирование используют одну форму ProductForm и один шаблон.
- ContactsView: страница контактов с данными из модели ContactInfo и
  обработкой формы обратной связи (View — отдельные get()/post()).
"""

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from catalog.forms import ProductForm
from catalog.models import ContactInfo, Product

PRODUCTS_PER_PAGE = 6


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

        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная"
        return context


class ProductDetailView(DetailView):
    """Страница с подробной информацией о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


class ProductCreateView(CreateView):
    """Форма добавления нового товара."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить товар"
        return context


class ProductUpdateView(UpdateView):
    """Редактирование товара; после сохранения — на страницу товара."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать товар"
        return context


class ProductDeleteView(DeleteView):
    """Удаление товара с подтверждением; после удаления — на главную."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

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
