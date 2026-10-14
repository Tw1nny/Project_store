"""
URL-адреса приложения catalog.

Подключается в основной urls.py проекта через include("catalog.urls").
"""

from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/add/", views.product_create, name="product_create"),
    path("contacts/", views.contacts, name="contacts"),
]
