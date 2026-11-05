"""
Формы приложения users.

- UserRegisterForm — регистрация: email, пароль и подтверждение пароля.
  Пароли сверяются и проверяются стандартными валидаторами Django
  (длина, слишком простой пароль, только цифры и т. п.).
- UserLoginForm — вход по email и паролю с понятными сообщениями
  об ошибках.
- UserProfileForm — редактирование профиля (доп. задание): имя,
  фамилия, аватар, телефон, страна.
- UserAdminCreationForm / UserAdminChangeForm — формы для админки,
  рассчитанные на модель без поля username.

Стили полей назначаются в __init__ через общий StyleFormMixin.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from catalog.forms import StyleFormMixin, validate_uploaded_image
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"placeholder": "you@example.com", "autofocus": True})
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"
        self.fields["password2"].help_text = "Введите тот же пароль ещё раз."

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    error_messages = {
        "invalid_login": "Неверный email или пароль. Обратите внимание: пароль чувствителен к регистру.",
        "inactive": "Этот аккаунт отключён.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs["placeholder"] = "you@example.com"
        self.fields["password"].label = "Пароль"


class UserProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar", "phone_number", "country")
        help_texts = {
            "avatar": "Формат JPEG или PNG, размер не больше 5 МБ.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].widget.attrs["placeholder"] = "+7 999 123-45-67"
        self.fields["avatar"].widget.attrs["accept"] = ".jpg,.jpeg,.png"

    def clean_avatar(self):
        return validate_uploaded_image(self.cleaned_data.get("avatar"))


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
