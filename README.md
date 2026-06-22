# ClientRelate

> 🇬🇧 English | [🇷🇺 Русский](README.ru.md)

ClientRelate is a web-based CRM and support-ticket system built with Django. It lets authenticated users submit feedback, open support tickets, and post proposals — and receive notifications from administrators.

## Features

- User registration and authentication
- Submit **feedback**, **support tickets**, and **proposals** through a unified form
- View personal interaction history with filtering by type and pagination
- Receive and dismiss personal **notifications**
- Full **admin panel** with search, filters, and list views for all entities
- Dark-themed responsive UI built on Bootstrap 5

## Tech Stack

| Layer     | Technology                   |
|-----------|------------------------------|
| Backend   | Python 3, Django 3.2 (LTS)  |
| Database  | SQLite (default)             |
| Frontend  | Bootstrap 5, HTML5 templates |
| Admin UI  | django-admin-tailwind        |

## Getting Started

**Prerequisites:** Python 3.9+

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

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

## Project Structure

```
config/            Django project configuration
crm/
  models.py        Database models
  views.py         View functions
  forms.py         Form classes
  admin.py         Admin registrations
  templates/       HTML templates
  migrations/      Database migrations
static/            Static files (CSS, JS)
```

## Running Tests

```bash
python manage.py test crm
```

## Environment Variables

For production, set the following environment variables:

| Variable        | Description                      |
|-----------------|----------------------------------|
| `SECRET_KEY`    | Django secret key                |
| `DEBUG`         | Set to `False` in production     |
| `ALLOWED_HOSTS` | Comma-separated list of domains  |

## License

[MIT](LICENSE)
