"""
Кастомная команда для наполнения базы тестовыми данными.

Перед загрузкой новых данных полностью удаляет существующие записи
Product и Category (в этом порядке, чтобы не упереться в FK), а затем
загружает фикстуры через стандартный loaddata.

Запуск:
    python manage.py fill_catalog
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет все продукты и категории, затем загружает фикстуры catalog/fixtures/*.json"

    def handle(self, *args, **options):
        self.stdout.write("Удаление существующих данных...")
        # Сначала продукты (у них FK на категорию), потом категории.
        deleted_products, _ = Product.objects.all().delete()
        deleted_categories, _ = Category.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(
                f"  удалено продуктов: {deleted_products}, категорий: {deleted_categories}"
            )
        )

        self.stdout.write("Загрузка фикстур...")
        call_command("loaddata", "categories.json")
        call_command("loaddata", "products.json")

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: категорий — {Category.objects.count()}, "
                f"продуктов — {Product.objects.count()}."
            )
        )
