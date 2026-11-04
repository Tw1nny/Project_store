from django.contrib import admin

from catalog.models import Category, ContactInfo, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "owner", "is_published")
    list_filter = ("category", "is_published")
    # Публиковать товары можно прямо из списка в админке.
    list_editable = ("is_published",)
    search_fields = ("name", "description")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "phone", "email")
