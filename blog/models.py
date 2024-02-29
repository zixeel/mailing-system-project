from django.conf import settings
from django.db import models

from main.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    slug = models.CharField(verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(verbose_name='preview', upload_to='blog/', **NULLABLE)
    date_of_birth = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='просмотров')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Creator')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('view_count',)
