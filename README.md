# Asynchronous Email Processing

A Django example application that moves email sending out of the web request cycle using Celery and Redis. A contact form submits a background task, while Celery Beat supports scheduled tasks and Flower provides a worker-monitoring interface.

## Features

- Django contact form with server-side form validation
- Background email delivery through a Celery task
- Redis as the Celery message broker
- Celery Beat with django-celery-beat for scheduled task management
- Flower dashboard for inspecting Celery workers and tasks
- Docker Compose configuration for the web app, Redis, worker, scheduler, and Flower

## Technology

- Python 3.10 (Docker base image)
- Django
- Celery
- Redis
- django-celery-beat
- Flower
- Docker Compose
- Gunicorn and Nginx configuration files are included

## Run with Docker Compose

### Prerequisites

- Docker
- Docker Compose

Create a `.env` file in the repository root. Configure the Redis broker and your email provider settings. For the Compose network, the Redis hostname is `redis`.

Example:

```dotenv
CELERY_BROKER_URL=redis://redis:6379/0

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
```

Build and start the services:

```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
```

Open the application at [http://localhost:8000](http://localhost:8000). The Flower dashboard is available at [http://localhost:5555](http://localhost:5555).

Useful commands:

```bash
docker compose ps
docker compose logs -f web
docker compose logs -f celery
docker compose logs -f celery-beat
docker compose logs -f flower
docker compose down
```

## Run locally

1. Create and activate a Python virtual environment.
2. Install the dependencies with `python -m pip install -r requirements.txt`.
3. Start a local Redis server and set `CELERY_BROKER_URL=redis://localhost:6379/0` in the application environment.
4. Configure the email settings in the environment.
5. Apply migrations with `python manage.py migrate`.
6. Start Django with `python manage.py runserver`.
7. In separate terminals, start the worker and scheduler:

```bash
celery -A async_email_project worker -l info
celery -A async_email_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A async_email_project flower --port=5555
```

## How the flow works

1. A user submits the contact form.
2. Django validates the submitted email address and message.
3. The view queues the `send_contact_email` task using Celery.
4. The Celery worker processes the task and sends the email through Django's configured email backend.
5. Flower can be used to inspect worker activity.

## Configuration and deployment notes

- The repository's default database configuration uses SQLite.
- Configure a real SMTP provider before expecting email delivery; the console email backend is useful for local development.
- Review the Django secret key, debug mode, allowed hosts, email recipient, and other deployment settings before exposing the application publicly.
- Do not commit real email credentials or secret keys.
