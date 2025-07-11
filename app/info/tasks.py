from celery import shared_task
from django.core.mail import send_mail

from info.settings import ADMIN_EMAIL

from .models import ContactMessage


@shared_task
def send_contact_email(message_id, recipient_email):
    """
    Задача для отправки email-уведомления о новом сообщении обратной связи.
    """
    try:
        message_obj = ContactMessage.objects.get(id=message_id)
    except ContactMessage.DoesNotExist:
        return False

    subject = f"Новое сообщение с сайта от {message_obj.name}"
    message = (
        f"Получено новое сообщение через форму обратной связи:\n\n"
        f"Имя: {message_obj.name}\n"
        f"Email: {message_obj.email}\n\n"
        f"Сообщение:\n{message_obj.message}\n\n"
        f"Дата отправки: {message_obj.created_at}"
    )
    mail_sent = send_mail(
        subject,
        message,
        ADMIN_EMAIL,
        [recipient_email],  # Список получателей
        fail_silently=False,
    )
    return mail_sent
