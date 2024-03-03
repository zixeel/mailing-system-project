from django.contrib import admin
from main.models import Client, Message, Mail, Logs
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject',)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'frequency', 'status',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'attempt_status', 'mail_server_response',)
