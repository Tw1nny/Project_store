"""
Контроллеры приложения catalog.

- home: отображает главную страницу интернет-магазина, выводит в
  консоль 5 последних добавленных продуктов (дополнительное задание).
- contacts: отображает страницу контактов с данными из модели
  ContactInfo (дополнительное задание) и обрабатывает отправку формы
  обратной связи — данные печатаются в консоль, пользователю
  показывается сообщение об успешной отправке.
"""

from django.shortcuts import render

from catalog.models import ContactInfo, Product


def home(request):
    """Главная страница."""
    latest_products = Product.objects.select_related("category").order_by("-created_at")[:5]

    print("Последние 5 добавленных продуктов:")
    for product in latest_products:
        print(f"  [{product.id}] {product.name} — {product.price} ({product.category.name})")

    context = {
        "title": "Главная",
        "latest_products": latest_products,
    }
    return render(request, "catalog/home.html", context)


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
