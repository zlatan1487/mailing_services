from django.db import models
from django.db import models
from django.conf import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    """
    Клиент сервиса:
        контактный email,
        ФИО,
        комментарий.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    email = models.EmailField(max_length=255, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, **NULLABLE, verbose_name='Отчество')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Mailing(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    )

    mailing_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время и дата рассылки')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Создатель', related_name='mailings')
    clients = models.ManyToManyField('Customer', related_name='mailings', verbose_name='Клиенты')
    message = models.ForeignKey('MailText', on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return f"Рассылка ({self.frequency})"


class MailText(models.Model):
    """
    Сообщение для рассылки:
        тема письма,
        тело письма.
    """
    topic = models.CharField(max_length=100, verbose_name='Тема рассылки', unique=True)  # Добавлено unique=True
    message = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return self.topic


class MailingLog(models.Model):
    STATUS_CHOICES = (
        ('success', 'Успех'),
        ('failure', 'Ошибка'),
    )

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус попытки')
    server_response = models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_logs')

    def __str__(self):
        return f"{self.timestamp}, Статус: {self.status})"


