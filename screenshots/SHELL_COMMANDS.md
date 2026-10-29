# Задание 5 — работа с Django shell

Эти команды нужно выполнить **у себя локально** (после того как
поднят PostgreSQL и применены миграции), по очереди, и после каждого
блока сделать скриншот терминала. Скриншоты сохраните в папку
`screenshots/` (например: `screenshots/01_categories.png`,
`screenshots/02_products.png` и т.д.) и закоммитьте в репозиторий.

Запуск shell (рекомендуется `ipython`, он уже в зависимостях —
Django сам его подхватит как более удобную оболочку):

```bash
python manage.py shell
```

## 1. Создание категорий через create()

```python
from catalog.models import Category, Product

cat_electronics = Category.objects.create(
    name="Электроника",
    description="Смартфоны, ноутбуки и другая техника.",
)
cat_clothes = Category.objects.create(
    name="Одежда",
    description="Повседневная и спортивная одежда.",
)
```

## 2. Создание продуктов через create()

```python
p1 = Product.objects.create(
    name="Смартфон Galaxy A55",
    description="6.6-дюймовый экран, 128 ГБ памяти.",
    category=cat_electronics,
    price=29990,
)
p2 = Product.objects.create(
    name="Худи унисекс",
    description="Тёплое худи из хлопка.",
    category=cat_clothes,
    price=2490,
)
```

## 3. Получить все категории

```python
Category.objects.all()
```

## 4. Получить все продукты

```python
Product.objects.all()
```

## 5. Все продукты определённой категории

```python
Product.objects.filter(category=cat_electronics)
# или по имени категории:
Product.objects.filter(category__name="Электроника")
```

## 6. Обновление цены определённого продукта

```python
p1.price = 27990
p1.save()

# либо одной строкой через update():
Product.objects.filter(pk=p1.pk).update(price=27990)
```

## 7. Удаление продукта

```python
p2.delete()
```

---

После выполнения всех пунктов сделайте финальный скриншот со списком
файлов в `screenshots/`, чтобы наставник видел, что все шаги покрыты.
