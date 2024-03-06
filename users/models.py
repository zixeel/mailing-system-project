from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import NULLABLE


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    username = None
    phone = models.CharField(max_length=35, verbose_name='Phone', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Account is  activated', **NULLABLE)
    token = models.CharField(max_length=32, verbose_name='Token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        permissions = [
            ('set_is_active', 'Может блокировать пользователей сервиса'),
        ]