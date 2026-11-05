from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    verbose_name = "Каталог товаров"

    def ready(self):
        # Подключаем сигналы, которые сбрасывают кеш при изменении товаров.
        import catalog.signals  # noqa: F401
