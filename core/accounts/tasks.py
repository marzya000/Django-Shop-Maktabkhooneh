from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email(subject, text_message, html_message, from_email, recipient_list):    

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=from_email,
        to=recipient_list,
    )

    email.attach_alternative(html_message, "text/html")

    email.send(fail_silently=False)