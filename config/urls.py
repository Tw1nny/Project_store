"""
Основной URL-файл проекта.

Все маршруты приложения catalog подключаются через include(),
как того требует задание. Собственные адреса контроллеров
(главная, контакты) описаны в catalog/urls.py.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),
]
