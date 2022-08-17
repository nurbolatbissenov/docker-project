from config.celery import celery_app
from django.core.mail import send_mail


@celery_app.task(name="custom_send_mail",
                 bind=True,
                 default_retry_delay=5,
                 max_retries=1)
def custom_send_mail(self, email: str):
    send_mail(
        'SUBJECT-111',
        'Here is the message. bla-bla-bla',
        'nurbolat_92@inbox.ru',
        [email],
        fail_silently=False,
    )