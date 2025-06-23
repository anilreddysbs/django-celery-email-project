
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_email_project.settings')

app = Celery('async_email_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Optional: Periodic task definition (only for static config; not needed for django-celery-beat)
# app.conf.beat_schedule = {
#     'send-test-email-every-10-seconds': {
#         'task': 'contact.tasks.send_test_email',
#         'schedule': 10.0,
#     },
# }

app.conf.timezone = 'UTC'

