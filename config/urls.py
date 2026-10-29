"""
Основной URL-файл проекта.

Маршруты приложений подключаются через include():
- catalog — главная, товары, контакты (catalog/urls.py);
- blog — все адреса под префиксом blogs/ (blog/urls.py).
Все URL проекта заканчиваются на «/».
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blogs/", include("blog.urls")),
    path("", include("catalog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
