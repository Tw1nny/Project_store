"""
URL-адреса приложения catalog.

Подключается в основной urls.py проекта через include("catalog.urls").
Контроллеры реализованы как CBV (урок 5).
"""

from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/add/", views.ProductCreateView.as_view(), name="product_create"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
]
