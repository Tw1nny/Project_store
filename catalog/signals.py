"""
Сигналы, которые сбрасывают кеш, когда меняются товары или категории.

Без них после редактирования товара сайт до 15 минут показывал бы
старые данные из Redis.
"""

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from catalog.models import Category, Product
from catalog.services import invalidate_category_cache, invalidate_product_page


@receiver(pre_save, sender=Product)
def remember_old_category(sender, instance, **kwargs):
    # Если товар перенесли в другую категорию, кеш нужно сбросить у обеих.
    instance._old_category_id = None
    if instance.pk:
        instance._old_category_id = (
            Product.objects.filter(pk=instance.pk).values_list("category_id", flat=True).first()
        )


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    invalidate_category_cache(instance.category_id, getattr(instance, "_old_category_id", None))
    invalidate_product_page(instance.pk)


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    invalidate_category_cache(instance.pk)
    # Название категории выводится на страницах её товаров.
    if kwargs.get("signal") is post_save:
        invalidate_product_page(*instance.products.values_list("pk", flat=True))
