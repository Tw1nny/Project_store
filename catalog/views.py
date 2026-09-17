"""
Контроллеры приложения catalog.

- home: отображает главную страницу интернет-магазина.
- contacts: отображает страницу контактов и обрабатывает отправку
  формы обратной связи (дополнительное задание) — данные из формы
  печатаются в консоль, а пользователю показывается сообщение об
  успешной отправке.
"""

from django.shortcuts import render


def home(request):
    """Главная страница."""
    context = {
        "title": "Главная",
    }
    return render(request, "catalog/home.html", context)


def contacts(request):
    """Страница контактов + обработка формы обратной связи."""
    context = {
        "title": "Контакты",
        "success": False,
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
