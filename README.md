# Интернет-магазин — учебный проект

Учебный проект интернет-магазина, который дорабатывается на каждом
уроке курса. Репозиторий содержит несколько этапов разработки:

1. **`server.py`** — минимальное веб-приложение на `http.server`, без
   фреймворков (урок 1).
2. **`config/` + `catalog/`** — Django-проект с приложением `catalog`
   (урок 2): страницы «Главная» и «Контакты», рендер через `render()`.
3. **PostgreSQL, модели, админка, фикстуры** (урок 3, текущий) —
   подключена БД PostgreSQL, созданы модели `Category`/`Product`,
   настроена админка, добавлены фикстуры и кастомная management-команда.

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
│   ├── views.py                   # home(), contacts()
│   ├── urls.py
│   ├── migrations/
│   │   └── 0001_initial.py        # миграция моделей
│   ├── fixtures/
│   │   ├── categories.json
│   │   └── products.json
│   ├── management/commands/
│   │   └── fill_catalog.py        # очищает БД и грузит фикстуры
│   └── templates/catalog/
│       ├── base.html
│       ├── home.html
│       └── contacts.html          # выводит ContactInfo из БД
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

   - `http://127.0.0.1:8000/` — главная страница (в консоли увидите
     список последних 5 продуктов);
   - `http://127.0.0.1:8000/contacts/` — контакты (данные из
     `ContactInfo`, заполняются через админку) + форма обратной связи;
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
