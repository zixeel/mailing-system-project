from datetime import time

from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Message(models.Model):
    message_title = models.CharField(verbose_name='Title', max_length=200)
    message_text = models.TextField(verbose_name='Message text')

    def __str__(self):
        return f" {self.message_title}, {self.message_text[:100]}..."

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Client(models.Model):
    first_name = models.CharField(verbose_name='Name', max_length=100)
    last_name = models.CharField(verbose_name='Last name', max_length=100, **NULLABLE)
    surname = models.CharField(verbose_name='Surname', max_length=100, **NULLABLE)
    email = models.EmailField(verbose_name='Emai', max_length=100)
    comments = models.TextField(verbose_name='Comments', **NULLABLE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        verbose_name='Creator', **NULLABLE)

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name} {self.surname}  ({self.email})'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Mail(models.Model):
    FREQUENCY_CHOICES = (
        ('ONCE_A_DAY', 'once a day '),
        ('ONCE_A_WEEK', 'once a week'),
        ('ONCE_A_MONTH', 'once a month')
    )

    STATUS_CHOICES = (
        ('CREATED', 'created'),
        ('COMPLETE', 'complete'),
        ('RUNING', 'runing'),
    )

    start_time = models.DateTimeField(verbose_name='start')
    end_time = models.DateTimeField(verbose_name='end')
    frequency = models.CharField(verbose_name='Frequency', choices=FREQUENCY_CHOICES)
    status = models.CharField(verbose_name='Status', choices=STATUS_CHOICES, default='CREATED')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='creator',
                                **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='message', **NULLABLE)
    clients = models.ManyToManyField(Client, verbose_name='clients')

    def __str__(self):
        return f"{self.frequency}, {self.status},{self.start_time}"

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailings'


class Logs(models.Model):
    STATUS_CHOICES = (
        ('SUCCESS', 'success'),
        ('FAILURE', 'failure')
    )
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, **NULLABLE)
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='Mail', related_name='logs')
    status = models.CharField(verbose_name='Status', choices=STATUS_CHOICES, **NULLABLE)
    server_response = models.TextField(verbose_name='Server Response', **NULLABLE)

    def __str__(self):
        return f"{self.created_at}, {self.status},{self.server_response}"

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
