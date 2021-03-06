from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class News(models.Model):
    STATUS_CHOICES = [
        ('a', 'active'),
        ('n', 'not_active')
    ]
    title = models.CharField(max_length=500, db_index=True, verbose_name='Заголовок')
    content = models.TextField(max_length=3000, default='', verbose_name='Новость')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата редактирования')
    flag_active = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n', verbose_name='Флаг активности')

    def get_absolute_url(self):
        return reverse('news')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news'
        ordering = ['created_at']
        verbose_name_plural = 'Новости'  # Переименовываем в админ-панели название таблицы с News на Новости


class Comments(models.Model):
    name = models.CharField(max_length=500, db_index=True, blank=True, verbose_name='Имя пользователя')
    text = models.TextField(max_length=3000, default='', verbose_name='Комментарий')
    news = models.ForeignKey('News', on_delete=models.CASCADE,
                             verbose_name='Комментируемая новость')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             verbose_name='Пользователь')

    class Meta:
        db_table = 'comments'
        verbose_name_plural = 'Комментарии'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=36, blank=True, verbose_name='Город')
    flag_verification = models.BooleanField(blank=True, default=False, verbose_name='Флаг верификации')
    count_news = models.IntegerField(blank=True, default=0, verbose_name='Кол-во опубликованных новостей')

    class Meta:
        db_table = 'profile'
        verbose_name_plural = 'Дополнительные данные пользователя'
        permissions = (
            ("can_verification_user", "Может проверить пользователя"),
        )

    def __str__(self):
        return self.user
