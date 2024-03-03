from datetime import timedelta
from django.utils import timezone
from main.models import Mail
from main.services import mailing_send


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

    for mail in mailing:
        if mail.logs:
            date_diff = current_datetime - mail.logs.last().date
            if date_diff >= timedelta(days=1) and mail.frequency == 'ONCE_A_DAY':
                mailing_send(mail)
            elif date_diff >= timedelta(days=7) and mail.frequency == 'ONCE_A_WEEK':
                mailing_send(mail)
            elif date_diff >= timedelta(days=30) and mail.frequency == 'ONCE_A_MONTH':
                mailing_send(mail)
            else:
                pass
        else:
            mailing_send(mail)


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