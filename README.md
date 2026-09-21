# Интернет-магазин — учебный проект

Учебный проект интернет-магазина, который дорабатывается на каждом
уроке курса. Репозиторий содержит два этапа разработки:

1. **`server.py`** — минимальное веб-приложение на встроенном модуле
   `http.server`, без использования фреймворков (задание урока 1).
2. **`config/` + `catalog/`** — полноценный Django-проект с приложением
   `catalog`, тем же интернет-магазином, но уже на фреймворке
   (задание урока 2). Это текущая, актуальная версия проекта.

Оба слоя оставлены в репозитории для истории выполнения домашних
заданий; для проверки текущего задания используется Django-часть.

## Стек технологий

- Python 3.11+
- Django 5.x (для актуальной версии проекта)
- Bootstrap 5 (подключается с CDN)
- SQLite (база данных Django по умолчанию)

## Структура проекта

```
.
├── manage.py                  # запуск Django-проекта
├── requirements.txt           # Django (для server.py зависимостей не нужно)
├── .gitignore
├── README.md
│
├── config/                    # НАСТРОЙКИ Django-проекта
│   ├── settings.py             # catalog зарегистрирован в INSTALLED_APPS
│   ├── urls.py                 # include("catalog.urls")
│   ├── wsgi.py
│   └── asgi.py
│
├── catalog/                   # Django-приложение каталога товаров
│   ├── views.py                 # контроллеры home() и contacts()
│   ├── urls.py                  # "" (главная) и "contacts/" (контакты)
│   ├── apps.py
│   ├── models.py
│   ├── admin.py
│   └── templates/catalog/
│       ├── base.html            # общий хедер (сайдбар) + футер, Bootstrap
│       ├── home.html            # главная страница
│       └── contacts.html        # страница контактов + форма обратной связи
│
├── server.py                  # ПРЕДЫДУЩЕЕ задание: сервер на http.server
└── templates/                 # шаблоны для server.py (не используются Django)
    ├── index.html
    ├── catalog.html
    ├── category.html
    ├── contacts.html
    └── style.css
```

## Как запустить актуальную версию (Django)

1. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Примените миграции:

   ```bash
   python manage.py migrate
   ```

4. Запустите сервер разработки:

   ```bash
   python manage.py runserver
   ```

5. Откройте в браузере:
   - `http://127.0.0.1:8000/` — главная страница;
   - `http://127.0.0.1:8000/contacts/` — страница контактов с формой
     обратной связи.

### Функциональность Django-приложения

- **Главная страница** (`/`) — рендерится функцией `render()` через
  `catalog/templates/catalog/home.html`.
- **Страница контактов** (`/contacts/`) — рендерится функцией
  `render()` через `catalog/templates/catalog/contacts.html`.
- **Форма обратной связи** — POST на `/contacts/` считывает поля
  `name`, `email`, `message`, печатает их в консоль сервера и
  показывает на странице сообщение об успешной отправке.

## Как запустить предыдущую версию (`server.py`, без Django)

Оставлено для истории/сравнения — задание прошлого урока.

```bash
python server.py
```

Сервер слушает `http://localhost:8000/` и на любой GET-запрос отдаёт
страницу «Контакты» из папки `templates/`; POST печатает данные формы
в консоль. Подробности — в коде `server.py`.

## Работа с Git

Разработка ведётся по GitFlow: ветка `main` — стабильный релиз,
`develop` — интеграционная ветка, отдельные ветки — под каждое домашнее
задание (например, `homework/lesson-2-django-setup`). Pull request
отправляется из ветки домашнего задания в `develop`.

## Соответствие критериям текущего задания (Django)

| Критерий | Где реализовано |
|---|---|
| `.gitignore` (`.idea`, `venv/`, `__pycache__/`, `env/`, sqlite) | `.gitignore` |
| README с описанием проекта | этот файл |
| Файл с зависимостями | `requirements.txt` |
| Django-проект создан | `config/`, `manage.py` |
| Приложение `catalog` создано и зарегистрировано | `catalog/`, `config/settings.py` → `INSTALLED_APPS` |
| `urls.py` в приложении `catalog` | `catalog/urls.py` |
| HTML-шаблон главной страницы, Bootstrap, порядок элементов | `catalog/templates/catalog/home.html`, `base.html` |
| Контроллер главной страницы через `render()` на `/` | `catalog/views.py` → `home()` |
| Контроллер контактов через `render()` на `contacts/` | `catalog/views.py` → `contacts()` |
| `include()` в основном `urls.py` | `config/urls.py` |
| Все URL заканчиваются на `/` | `catalog/urls.py`, `config/urls.py` |
| Доп. задание: форма обратной связи | `catalog/templates/catalog/contacts.html`, `catalog/views.py` |
