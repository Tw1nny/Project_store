"""
Контроллеры приложения catalog.

- home: главная страница — постранично выводит список товаров
  (Product.objects.all(), пагинация через Paginator), а также печатает
  в консоль 5 последних добавленных продуктов (доп. задание прошлого
  урока).
- product_detail: страница с подробной информацией о товаре по pk.
- product_create: форма добавления нового товара (доп. задание).
- contacts: страница контактов с данными из модели ContactInfo и
  обработкой формы обратной связи.
"""

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from catalog.forms import ProductForm
from catalog.models import ContactInfo, Product

PRODUCTS_PER_PAGE = 6


def home(request):
    """Главная страница — список товаров с пагинацией."""
    latest_products = Product.objects.select_related("category").order_by("-created_at")[:5]

    print("Последние 5 добавленных продуктов:")
    for product in latest_products:
        print(f"  [{product.id}] {product.name} — {product.price} ({product.category.name})")

    products_qs = Product.objects.all()
    paginator = Paginator(products_qs, PRODUCTS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "Главная",
        "page_obj": page_obj,
        "products": page_obj.object_list,
    }
    return render(request, "catalog/home.html", context)


def product_detail(request, pk):
    """Страница с подробной информацией о товаре."""
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    context = {
        "title": product.name,
        "product": product,
    }
    return render(request, "catalog/product_detail.html", context)


def product_create(request):
    """Форма добавления нового товара."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("catalog:product_detail", pk=product.pk)
    else:
        form = ProductForm()

    context = {
        "title": "Добавить товар",
        "form": form,
    }
    return render(request, "catalog/product_form.html", context)


def contacts(request):
    """Страница контактов + обработка формы обратной связи."""
    contact_info = ContactInfo.objects.first()

    context = {
        "title": "Контакты",
        "success": False,
        "contact_info": contact_info,
    }

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        print("Получены данные формы обратной связи:")
        print(f"  Имя: {name}")
        print(f"  Почта: {email}")
        print(f"  Сообщение: {message}")

        context["success"] = True
        context["name"] = name

    return render(request, "catalog/contacts.html", context)
