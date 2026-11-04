"""
URL-адреса приложения users.

Подключается в config/urls.py через path("users/", include("users.urls")).
"""

from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileUpdateView.as_view(), name="profile"),
]
