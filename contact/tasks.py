
from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_contact_email(subject, message, from_email):
    send_mail(
        subject,
        message,
        from_email,
        ['sbsanilreddy@gmail.com'],  # change to your destination email
        fail_silently=False,
    )


@shared_task
def send_test_email():
    print("💥 Celery Beat ran this task!")
