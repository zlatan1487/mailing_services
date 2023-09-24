from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=30, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=100, blank=True, verbose_name='Страна')
    is_blocked = models.BooleanField(default=False, verbose_name='Блокирован')  # Поле для хранения информации о блокировке пользователя

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

