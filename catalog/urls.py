"""
URL-адреса приложения catalog.

Подключается в основной urls.py проекта через include("catalog.urls").
"""

from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
]
