"""
Основной URL-файл проекта.

Все маршруты приложения catalog подключаются через include(),
как того требует задание. Собственные адреса контроллеров
(главная, контакты) описаны в catalog/urls.py.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
