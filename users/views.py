"""
Контроллеры приложения users (CBV).

- RegisterView: регистрация. После создания аккаунта пользователь сразу
  входит в систему, а на его почту уходит приветственное письмо. Если
  письмо отправить не удалось, аккаунт всё равно создаётся, а
  пользователь видит предупреждение.
- UserLoginView: вход по email и паролю.
- LogoutView (стандартный, в urls.py): выход, только POST-запросом.
- ProfileUpdateView: редактирование профиля (доп. задание).
"""

import logging
import smtplib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import User

logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        # Уже вошедшему пользователю регистрироваться повторно незачем.
        if request.user.is_authenticated:
            return redirect("catalog:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        self.send_welcome_email(self.object)
        messages.success(self.request, "Регистрация прошла успешно. Добро пожаловать!")
        return redirect(self.get_success_url())

    def send_welcome_email(self, user):
        try:
            send_mail(
                subject="Добро пожаловать в наш интернет-магазин!",
                message=(
                    "Здравствуйте!\n\n"
                    f"Вы зарегистрировались в учебном интернет-магазине с адресом {user.email}.\n"
                    "Теперь вам доступны страницы товаров: просмотр, добавление и редактирование.\n\n"
                    "Спасибо, что вы с нами!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except (smtplib.SMTPException, OSError, BadHeaderError):
            logger.exception("Не удалось отправить приветственное письмо на %s", user.email)
            messages.warning(
                self.request,
                "Аккаунт создан, но приветственное письмо отправить не удалось. "
                "Проверьте адрес почты в профиле или попробуйте позже.",
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True
    extra_context = {"title": "Вход"}


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        # Редактировать можно только собственный профиль.
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль сохранён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Профиль"
        return context
