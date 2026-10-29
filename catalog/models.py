"""
Модели приложения catalog.

- Category — категория товара.
- Product — товар, связан с категорией через ForeignKey.
- ContactInfo — контактные данные компании (дополнительное задание),
  заполняются через админку и выводятся на странице "Контакты".
"""

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    """
    Контактные данные компании. Предполагается, что в базе будет
    одна запись, которую редактируют через админку, а на странице
    "Контакты" она отображается вместо статичного текста.
    """

    title = models.CharField(
        max_length=200,
        default="Наши контакты",
        verbose_name="Заголовок",
    )
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return self.title
