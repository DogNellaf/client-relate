# ClientRelate

> [English](#english) | [Русский](#russian)

---

## English

ClientRelate is a web-based CRM and support-ticket system built with Django. It lets authenticated users submit feedback, open support tickets, and post proposals — and receive notifications from administrators.

### Features

- User registration and authentication
- Submit **feedback**, **support tickets**, and **proposals** through a unified form
- View personal interaction history with filtering by type and pagination
- Receive and dismiss personal **notifications**
- Full **admin panel** with search, filters, and list views for all entities
- Dark-themed responsive UI built on Bootstrap 5

### Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | Python 3, Django 3.2 (LTS)   |
| Database  | SQLite (default)              |
| Frontend  | Bootstrap 5, HTML5 templates  |
| Admin UI  | django-admin-tailwind         |

### Getting Started

**Prerequisites:** Python 3.9+

```bash
# Clone the repository
git clone <repository-url>
cd ClientRelate

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser (for the admin panel)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

The admin panel is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### Project Structure

```
ClientRelate/          Django project configuration
App/
  models.py            Database models
  views.py             View functions
  forms.py             Form classes
  admin.py             Admin registrations
  templates/           HTML templates
  migrations/          Database migrations
static/                Static files (CSS, JS)
```

### Running Tests

```bash
python manage.py test App
```

### Environment Variables

For production, set the following environment variables:

| Variable          | Description                     |
|-------------------|---------------------------------|
| `SECRET_KEY`      | Django secret key               |
| `DEBUG`           | Set to `False` in production    |
| `ALLOWED_HOSTS`   | Comma-separated list of domains |

---

## Russian

<a name="russian"></a>

ClientRelate — веб-система управления клиентскими взаимодействиями (CRM) и тикетами поддержки, построенная на Django. Авторизованные пользователи могут отправлять обратную связь, создавать тикеты и предложения, а также получать уведомления от администраторов.

### Возможности

- Регистрация и аутентификация пользователей
- Отправка **обратной связи**, **тикетов поддержки** и **предложений** через единую форму
- Просмотр истории обращений с фильтрацией по типу и пагинацией
- Получение и скрытие личных **уведомлений**
- Полноценная **панель администратора** с поиском, фильтрами и списками для всех сущностей
- Адаптивный интерфейс в тёмной теме на Bootstrap 5

### Технологии

| Слой       | Технология                      |
|------------|---------------------------------|
| Backend    | Python 3, Django 3.2 (LTS)     |
| База данных| SQLite (по умолчанию)           |
| Frontend   | Bootstrap 5, HTML5-шаблоны      |
| Админ      | django-admin-tailwind            |

### Быстрый старт

**Требования:** Python 3.9+

```bash
# Клонировать репозиторий
git clone <repository-url>
cd ClientRelate

# Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя (для панели администратора)
python manage.py createsuperuser

# Запустить сервер разработки
python manage.py runserver
```

Откройте [http://127.0.0.1:8000](http://127.0.0.1:8000) в браузере.

Панель администратора доступна по адресу [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### Структура проекта

```
ClientRelate/          Конфигурация Django-проекта
App/
  models.py            Модели базы данных
  views.py             Функции-представления
  forms.py             Классы форм
  admin.py             Регистрация в панели администратора
  templates/           HTML-шаблоны
  migrations/          Миграции базы данных
static/                Статические файлы (CSS, JS)
```

### Запуск тестов

```bash
python manage.py test App
```

### Переменные окружения

Для продакшн-развёртывания задайте следующие переменные окружения:

| Переменная        | Описание                              |
|-------------------|---------------------------------------|
| `SECRET_KEY`      | Секретный ключ Django                 |
| `DEBUG`           | Установить в `False` для продакшн     |
| `ALLOWED_HOSTS`   | Список допустимых доменов через запятую |

---

## License

[MIT](LICENSE)
