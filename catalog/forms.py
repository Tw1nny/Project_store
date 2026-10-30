"""
Формы приложения catalog.

- FORBIDDEN_WORDS — список запрещённых слов (константа). Их нельзя
  использовать в названии и описании товара, регистр не учитывается.
- StyleFormMixin — стилизация полей формы через __init__: каждому полю
  назначается подходящий Bootstrap-класс (чекбокс — form-check-input,
  выпадающий список — form-select, остальные — form-control).
  Используется и в формах приложения blog.
- ProductForm — создание и редактирование товара: проверка запрещённых
  слов, неотрицательной цены и загружаемого изображения
  (JPEG/PNG, не больше 5 МБ).
"""

import os
import re

from django import forms
from django.core.files.uploadedfile import UploadedFile

from catalog.models import Product

FORBIDDEN_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)

MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE = MAX_IMAGE_SIZE_MB * 1024 * 1024
ALLOWED_IMAGE_FORMATS = ("JPEG", "PNG")
ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


VOWELS = "аеёиоуыэюяй"


def _stem(word):
    """Основа слова без окончания: «крипта» → «крипт», «полиция» → «полици»."""
    return word.rstrip(VOWELS) or word


def find_forbidden_words(text):
    """Возвращает запрещённые слова, найденные в тексте.

    - регистр не учитывается, «ё» приравнивается к «е» («Дёшево»);
    - сравнение идёт по основе слова, поэтому ловятся и другие формы:
      «крипту», «бесплатная», «полицию», «радары»;
    - слово должно начинаться с основы, чтобы «скрипт» не считался «криптой».
    """
    normalized = (text or "").lower().replace("ё", "е")
    tokens = re.findall(r"\w+", normalized)
    return [
        word
        for word in FORBIDDEN_WORDS
        if any(token.startswith(_stem(word)) for token in tokens)
    ]


class StyleFormMixin:
    """Добавляет Bootstrap-классы всем полям формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = "form-select"
            else:
                css_class = "form-control"
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        labels = {
            "name": "Наименование",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена",
        }
        help_texts = {
            "image": f"Формат JPEG или PNG, размер не больше {MAX_IMAGE_SIZE_MB} МБ.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Например, Ноутбук"
        self.fields["description"].widget.attrs["rows"] = 4
        self.fields["price"].widget.attrs["step"] = "0.01"
        self.fields["image"].widget.attrs["accept"] = ".jpg,.jpeg,.png"

    def _check_forbidden_words(self, field_name):
        value = self.cleaned_data.get(field_name)
        found = find_forbidden_words(value)
        if found:
            raise forms.ValidationError(
                "Нельзя использовать запрещённые слова: %(words)s.",
                params={"words": ", ".join(found)},
            )
        return value

    def clean_name(self):
        return self._check_forbidden_words("name")

    def clean_description(self):
        return self._check_forbidden_words("description")

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError(
                "Цена не может быть отрицательной. Укажите значение 0 или больше."
            )
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")

        # Новый файл не загружали: поле пустое, оставили прежнее изображение
        # или отметили «Очистить». Проверять нечего.
        if not isinstance(image, UploadedFile):
            return image

        if image.size > MAX_IMAGE_SIZE:
            size_mb = image.size / (1024 * 1024)
            raise forms.ValidationError(
                f"Файл весит {size_mb:.1f} МБ, а максимум — {MAX_IMAGE_SIZE_MB} МБ."
            )

        extension = os.path.splitext(image.name)[1].lower()
        # Django уже открыл файл через Pillow и сохранил результат в image.image,
        # поэтому проверяем и расширение, и реальный формат содержимого.
        image_format = getattr(getattr(image, "image", None), "format", None)
        if extension not in ALLOWED_IMAGE_EXTENSIONS or image_format not in ALLOWED_IMAGE_FORMATS:
            raise forms.ValidationError("Можно загрузить только изображение в формате JPEG или PNG.")

        return image
