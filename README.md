# Интернет-магазин — учебный проект

Учебный проект интернет-магазина, который дорабатывается на каждом
уроке курса. Репозиторий содержит несколько этапов разработки:

1. **`server.py`** — минимальное веб-приложение на `http.server`, без
   фреймворков (урок 1).
2. **`config/` + `catalog/`** — Django-проект с приложением `catalog`
   (урок 2): страницы «Главная» и «Контакты», рендер через `render()`.
3. **PostgreSQL, модели, админка, фикстуры** (урок 3) — подключена
   БД PostgreSQL, созданы модели `Category`/`Product`, настроена
   админка, добавлены фикстуры и кастомная management-команда.
4. **Динамика и шаблоны** (урок 4) — детальная страница
   товара, общий базовый шаблон с подшаблоном меню, форма добавления
   товара, постраничный вывод списка товаров.
5. **CBV и блог** (урок 5) — все контроллеры `catalog`
   переписаны на классы, добавлено приложение `blog` с полным CRUD.
6. **Формы** (урок 6, текущий) — полный CRUD товаров на `django.forms`,
   запрет «спамных» слов, проверка цены и загружаемых изображений,
   стилизация полей через `__init__`.

Все слои оставлены в репозитории для истории выполнения домашних
заданий; актуальная функциональность — Django-часть с подключённой БД.

## Стек технологий

- Python 3.11+
- Django 5.x
- PostgreSQL + psycopg2-binary
- python-dotenv (переменные окружения)
- Pillow (работа с изображениями продуктов)
- ipython (удобный Django shell)
- Bootstrap 5 (подключается с CDN)

## Структура проекта

```
.
├── manage.py
├── requirements.txt
├── .env.example                 # шаблон переменных окружения (без секретов)
├── .gitignore                   # .env и db.sqlite* игнорируются
├── README.md
├── screenshots/                 # скриншоты работы в Django shell (задание 5)
│   └── SHELL_COMMANDS.md         # какие команды выполнить и заскриншотить
│
├── config/                      # настройки Django-проекта
│   ├── settings.py                # БД из .env, MEDIA_URL/MEDIA_ROOT
│   ├── urls.py                    # include("catalog.urls") + раздача media в DEBUG
│   ├── wsgi.py
│   └── asgi.py
│
├── catalog/                     # приложение каталога товаров
│   ├── models.py                  # Category, Product, ContactInfo
│   ├── admin.py                   # регистрация моделей в админке
│   ├── forms.py                   # ProductForm, FORBIDDEN_WORDS, StyleFormMixin
│   ├── views.py                   # HomeView, Product{Detail,Create,Update,Delete}View, ContactsView
│   ├── urls.py
│   ├── migrations/
│   │   └── 0001_initial.py        # миграция моделей
│   ├── fixtures/
│   │   ├── categories.json
│   │   └── products.json
│   ├── management/commands/
│   │   └── fill_catalog.py        # очищает БД и грузит фикстуры
│   └── templates/catalog/
│       ├── base.html              # общий шаблон: сайдбар + футер + стили
│       ├── includes/
│       │   └── menu.html          # подшаблон главного меню (include в base.html)
│       ├── home.html              # список товаров + пагинация
│       ├── product_detail.html    # подробная страница товара
│       ├── product_form.html      # форма создания/редактирования товара
│       ├── product_confirm_delete.html
│       └── contacts.html          # выводит ContactInfo из БД
│
├── blog/                        # приложение блога (урок 5)
│   ├── models.py                  # BlogPost
│   ├── admin.py
│   ├── forms.py                   # BlogPostForm
│   ├── views.py                   # List/Detail/Create/Update/DeleteView
│   ├── urls.py                    # всё под /blogs/
│   ├── migrations/0001_initial.py
│   └── templates/blog/            # list, detail, form, confirm_delete
│
├── server.py                    # задание урока 1 (http.server)
└── templates/                   # шаблоны для server.py
```

## Установка и запуск

1. Создайте и активируйте виртуальное окружение, установите зависимости:

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   pip install -r requirements.txt
   ```

2. Создайте базу данных PostgreSQL вручную (через `psql` или
   графический клиент), например:

   ```sql
   CREATE DATABASE store_db;
   CREATE USER store_user WITH PASSWORD 'change_me';
   GRANT ALL PRIVILEGES ON DATABASE store_db TO store_user;
   ```

3. Скопируйте `.env.example` в `.env` и подставьте свои данные
   подключения:

   ```bash
   cp .env.example .env      # Windows: copy .env.example .env
   ```

4. Примените миграции:

   ```bash
   python manage.py migrate
   ```

5. Создайте суперпользователя:

   ```bash
   python manage.py createsuperuser
   ```

6. (Опционально) наполните базу тестовыми данными из фикстур:

   ```bash
   python manage.py fill_catalog
   ```

7. Запустите сервер разработки:

   ```bash
   python manage.py runserver
   ```

   - `http://127.0.0.1:8000/` — главная страница: постраничный список
     товаров (в консоли увидите список последних 5 продуктов);
   - `http://127.0.0.1:8000/products/<id>/` — подробная страница товара;
   - `http://127.0.0.1:8000/products/add/` — форма добавления товара;
   - `http://127.0.0.1:8000/products/<id>/update/` и `.../delete/` —
     редактирование и удаление товара;
   - `http://127.0.0.1:8000/contacts/` — контакты (данные из
     `ContactInfo`, заполняются через админку) + форма обратной связи;
   - `http://127.0.0.1:8000/blogs/` — блог: только опубликованные статьи;
   - `http://127.0.0.1:8000/blogs/create/` — новая статья;
   - `http://127.0.0.1:8000/blogs/<id>/` — статья (каждое открытие +1 просмотр);
   - `http://127.0.0.1:8000/blogs/<id>/update/` и `.../delete/` — правка и удаление;
   - `http://127.0.0.1:8000/admin/` — админка Django.

## Работа с Django shell (задание 5)

Подробный список команд — в `screenshots/SHELL_COMMANDS.md`. Команды
нужно выполнить локально (`python manage.py shell`) и сохранить
скриншоты в папку `screenshots/`.

## Фикстуры и кастомная команда

```bash
# загрузить фикстуры вручную
python manage.py loaddata categories.json
python manage.py loaddata products.json

# либо одной командой — она сама чистит таблицы перед загрузкой
python manage.py fill_catalog
```

## Работа с Git

GitFlow: `main` — стабильный релиз, `develop` — интеграционная ветка,
отдельные ветки — под каждое домашнее задание. Pull request отправляется
из ветки домашки в `develop`. Файл `db.sqlite3` (если ранее коммитился)
удалён из репозитория и добавлен в `.gitignore` — БД теперь PostgreSQL.

## Соответствие критериям текущего задания

| Критерий | Где реализовано |
|---|---|
| Файл с зависимостями | `requirements.txt` |
| DATABASES → PostgreSQL (ENGINE/NAME/USER/PASSWORD/HOST/PORT) | `config/settings.py` |
| `psycopg2-binary` в зависимостях | `requirements.txt` |
| SQLite удалена из репозитория | нет `db.sqlite3` в репо, `.gitignore` |
| Настройки БД в `.env` | `config/settings.py` (`load_dotenv`), `.env` (не коммитится) |
| Шаблон `.env` | `.env.example` |
| Модель `Product` с нужными полями | `catalog/models.py` |
| Модель `Category` с нужными полями | `catalog/models.py` |
| `Meta` с `verbose_name`/`verbose_name_plural` | `catalog/models.py` |
| `__str__` в моделях | `catalog/models.py` |
| `Product.category` — `ForeignKey` | `catalog/models.py` |
| Миграции созданы и запушены | `catalog/migrations/0001_initial.py` |
| `MEDIA_URL`/`MEDIA_ROOT`, раздача в DEBUG | `config/settings.py`, `config/urls.py` |
| `Pillow` в зависимостях | `requirements.txt` |
| Продукты в админке: `id`, `name`, `price`, `category`, фильтр по категории, поиск по `name`/`description` | `catalog/admin.py` |
| Категории в админке: `id`, `name` | `catalog/admin.py` |
| `ipython` в зависимостях | `requirements.txt` |
| Скриншоты Shell | `screenshots/` (сохранить локально) |
| Фикстуры для `Category` и `Product` | `catalog/fixtures/*.json` |
| Кастомная команда, удаляет данные перед загрузкой, использует фикстуры | `catalog/management/commands/fill_catalog.py` |
| Доп. задание: 5 последних продуктов в консоль | `catalog/views.py` → `home()` |
| Доп. задание: модель контактов на странице | `catalog/models.py` → `ContactInfo`, `catalog/views.py`/`contacts.html` |

## Соответствие критериям урока 4 (динамика и шаблоны)

| Критерий | Где реализовано |
|---|---|
| Контроллер получает `pk`, извлекает объект через ORM, передаёт в шаблон | `catalog/views.py` → `product_detail()` |
| Название, описание, цена, изображение отображаются | `catalog/templates/catalog/product_detail.html` |
| URL `/products/<int:pk>/`, нейминг `product_detail` | `catalog/urls.py` |
| Лаконичный запрос `Product.objects.all()` для списка | `catalog/views.py` → `home()` |
| Цикл, изображение, название, описание (обрезано до 100 символов) | `catalog/templates/catalog/home.html` (`{% for %}`, `truncatechars:100`) |
| Переходы с главной на товар и обратно | ссылка «Подробнее» в `home.html`, «Назад к списку» в `product_detail.html` |
| Общий базовый шаблон, все шаблоны его наследуют | `catalog/templates/catalog/base.html`, `{% extends %}` во всех страницах |
| Подшаблон меню подключён во все шаблоны | `catalog/templates/catalog/includes/menu.html`, `{% include %}` в `base.html` |
| Доп.: форма добавления товара, валидация, сохранение в БД | `catalog/forms.py` (`ProductForm`), `catalog/views.py` → `product_create()`, `product_form.html` |
| Доп.: постраничный вывод товаров | `catalog/views.py` → `home()` (`Paginator`), блок пагинации в `home.html` |

## Соответствие критериям урока 5 (CBV и блог)

| Критерий | Где реализовано |
|---|---|
| Все контроллеры `catalog` — CBV | `catalog/views.py`: `HomeView` (ListView), `ProductDetailView` (DetailView), `ProductCreateView` (CreateView), `ContactsView` (View) |
| Контакты — через `View`/`TemplateView` | `ContactsView(View)` с методами `get()`/`post()` |
| Приложение `blog` создано и зарегистрировано | `blog/`, `INSTALLED_APPS` в `config/settings.py` |
| Модель `BlogPost`: заголовок, содержимое, превью, дата создания, признак публикации, просмотры | `blog/models.py` |
| `Meta` и `__str__` | `blog/models.py` |
| CRUD только на CBV | `blog/views.py` |
| Шаблоны наследуют базовый, меню подключено | `blog/templates/blog/*.html` → `{% extends "catalog/base.html" %}` |
| Маршруты под `blogs/`, `include()` в основном `urls.py` | `blog/urls.py`, `config/urls.py` |
| Все URL заканчиваются на `/` | `catalog/urls.py`, `blog/urls.py` |
| Счётчик просмотров через `get_object` | `BlogPostDetailView.get_object()` |
| Только опубликованные статьи через `get_queryset` | `BlogPostListView.get_queryset()` |
| После редактирования — на страницу статьи | `BlogPostUpdateView.get_success_url()` |
| Доп.: письмо при 100 просмотрах | `BlogPostDetailView.send_milestone_email()`, настройки почты в `config/settings.py` / `.env` |

По умолчанию письмо печатается в консоль `runserver`. Чтобы приходило на
настоящую почту, заполните блок «Почта» в `.env` (см. `.env.example`).

## Соответствие критериям урока 6 (формы)

| Критерий | Где реализовано |
|---|---|
| PR из ветки домашки в `develop`; `.env`, `__pycache__`, `.DS_Store` и др. в `.gitignore` | `.gitignore` |
| Зависимости в `requirements.txt`, лишнего нет | `requirements.txt` |
| Создание, просмотр, редактирование, удаление товаров | `catalog/views.py` → `ProductCreateView`, `ProductDetailView`, `ProductUpdateView`, `ProductDeleteView`; `catalog/urls.py` |
| Запрещённые слова вынесены в константу, проверяются в `name` и `description`, регистр игнорируется | `catalog/forms.py` → `FORBIDDEN_WORDS`, `clean_name()`, `clean_description()` |
| Отрицательная цена — понятная ошибка | `catalog/forms.py` → `clean_price()` |
| Стили у всех полей через `__init__`, чекбокс как элемент формы | `catalog/forms.py` → `StyleFormMixin` (чекбокс получает `form-check-input`, пример — «Опубликовано» в форме статьи блога) |
| Доп.: загрузка изображения, только JPEG/PNG, не больше 5 МБ | `catalog/forms.py` → `clean_image()` |
