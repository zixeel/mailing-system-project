from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from main.models import Mail
from main.models import Logs


def mailing_send(mail):
    """отправляет письмо"""
    try:
        send_mail(
            subject=mail.message.message_title,
            message=mail.message.message_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=mail.clients.values_list('email', flat=True),
            fail_silently=False,
        )
    # except SMTPException(OSError) as e:
    #     Logs.objects.create(status='FAILURE',
    #                         server_response=str(e),
    #                         mail=mail)
    except Exception as e:
        Logs.objects.create(status='FAILURE',
                            server_response=str(e),
                            mail=mail)
    else:
        Logs.objects.create(status='SUCCESS',
                            server_response='OK',
                            mail=mail)


def change_status_launched() -> None:
    current_datetime = timezone.now()
    mailing = Mail.objects.filter(status='CREATED',
                                  start_time__lte=current_datetime,
                                  end_time__gte=current_datetime)
    for mail in mailing:
        mail.status = 'RUNING'
        mail.save()


def mailing_in_frequency() -> None:
    current_datetime = timezone.now()
    mailing = Mail.objects.filter(status='RUNING')

    for maill in mailing:
        print(maill.logs)
        if maill.logs.exists():
            date_diff = current_datetime - maill.logs.last().created_at
            if date_diff >= timedelta(days=1) and maill.frequency == 'ONCE_A_DAY':
                mailing_send(maill)
            elif date_diff >= timedelta(days=7) and maill.frequency == 'ONCE_A_WEEK':
                mailing_send(maill)
            elif date_diff >= timedelta(days=30) and maill.frequency == 'ONCE_A_MONTH':
                mailing_send(maill)
            else:
                pass
        else:
            mailing_send(maill)


def change_status_completed() -> None:
    current_datetime = timezone.now()
    mailing = Mail.objects.filter(status='RUNING',
                                  end_time__lte=current_datetime)

    for mail in mailing:
        mail.status = 'COMPLETE'
        mail.save()


def main_job() -> None:
    change_status_launched()
    mailing_in_frequency()
    change_status_completed()
