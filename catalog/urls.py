"""
URL-адреса приложения catalog.

Подключается в основной urls.py проекта через include("catalog.urls").
Контроллеры реализованы как CBV. Все адреса заканчиваются на «/».

Страница товара кешируется (cache_product_page — обёртка над cache_page,
см. catalog/services.py).
"""

from django.urls import path

from catalog import views
from catalog.services import cache_product_page

app_name = "catalog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/add/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/",
        cache_product_page(views.ProductDetailView.as_view()),
        name="product_detail",
    ),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("categories/<int:pk>/", views.CategoryProductsView.as_view(), name="category_products"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
]
