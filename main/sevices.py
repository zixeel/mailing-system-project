from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings

from main.models import Logs


def mailing_send(mail):
    try:
        send_mail(
            subject=mail.message.message_title,
            message=mail.message.message_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=mail.clients.values_list('email', flat=True),
            fail_silently=False,
        )
    except SMTPException(OSError) as e:
        # Если возникает ошибка почтового сервиса записывает логи с ошибкой:
        Logs.objects.create(status='FAILURE',
                            server_response=str(e),
                            mail=mail)
    except Exception as e:
        # Записывает логи если возникла другая ошибка.
        Logs.objects.create(status='FAILURE',
                            server_response=str(e),
                            mail=mail)
    else:
        # Записывает успешные логи.
        Logs.objects.create(status='SUCCESS',
                            server_response='OK',
                            mail=mail)
