"""
URL-адреса приложения catalog.

Подключается в основной urls.py проекта через include("catalog.urls").
Контроллеры реализованы как CBV. Все адреса заканчиваются на «/».
"""

from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/add/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
]
