"""
Сервисный слой приложения catalog: работа с товарами и кешем (урок 9).

- get_products_by_category(category_id) — список всех опубликованных
  товаров категории. Низкоуровневое кеширование: результат хранится
  в Redis под ключом category_{id} в течение
  CATEGORY_PRODUCTS_CACHE_TIMEOUT секунд.
- cache_product_page(view) — кеширование страницы одного товара
  (cache_page). У каждого товара своя «версия» кеша: когда товар
  меняется, версия обновляется, и посетители сразу видят новую
  страницу, а не ждут, пока истечёт старый кеш.
- invalidate_category_cache / invalidate_product_page — сброс кеша,
  вызывается из сигналов (catalog/signals.py).
"""

import time
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from catalog.models import Product


# --- Список товаров категории (низкоуровневый кеш) ---

def category_cache_key(category_id):
    return f"category_{category_id}"


def get_products_by_category(category_id):
    """Возвращает список опубликованных товаров категории — из Redis или из БД."""
    key = category_cache_key(category_id)
    products = cache.get(key)
    if products is None:
        products = list(
            Product.objects.filter(category_id=category_id, is_published=True)
            .select_related("category", "owner")
        )
        cache.set(key, products, settings.CATEGORY_PRODUCTS_CACHE_TIMEOUT)
    return products


def invalidate_category_cache(*category_ids):
    keys = [category_cache_key(category_id) for category_id in category_ids if category_id]
    if keys:
        cache.delete_many(keys)


# --- Страница одного товара (кеш страницы) ---

def product_page_version_key(product_id):
    return f"product_page_version_{product_id}"


def cache_product_page(view):
    """cache_page для страницы товара с учётом версии товара и пользователя.

    - vary_on_cookie: у каждого пользователя своя копия страницы
      (в ней его email в меню и кнопки, доступные именно ему);
    - key_prefix с версией: после изменения товара старые копии
      страницы больше не используются.
    """

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        product_id = kwargs["pk"]
        version = cache.get(product_page_version_key(product_id), 0)
        cached_view = cache_page(
            settings.PRODUCT_PAGE_CACHE_TIMEOUT,
            key_prefix=f"product_{product_id}_v{version}",
        )(vary_on_cookie(view))
        return cached_view(request, *args, **kwargs)

    return wrapper


def invalidate_product_page(*product_ids):
    for product_id in product_ids:
        cache.set(product_page_version_key(product_id), time.time_ns(), None)
