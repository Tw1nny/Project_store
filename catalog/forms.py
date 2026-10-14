"""
Формы приложения catalog.

ProductForm — используется на странице добавления нового товара
(дополнительное задание урока 4). Поля обязательны (кроме изображения),
валидация выполняется стандартными средствами Django ModelForm.
"""

from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }
        labels = {
            "name": "Наименование",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена",
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price is not None and price <= 0:
            raise forms.ValidationError("Цена должна быть больше нуля.")
        return price
