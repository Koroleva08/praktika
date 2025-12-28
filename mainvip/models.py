from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    """Роль пользователя системы"""
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, verbose_name='Название роли')
    permissions = models.TextField(blank=True, null=True, verbose_name='Описание прав доступа')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        db_table = 'roles'

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    """Пользователь системы"""
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'
        # Делаем email уникальным
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]

    def __str__(self):
        return f"{self.full_name} ({self.username})"


class Organization(models.Model):
    """Организация"""
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Наименование организации')
    type = models.CharField(max_length=100, verbose_name='Тип организации')
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name='Адрес')
    website = models.CharField(max_length=150, blank=True, null=True, verbose_name='Веб-сайт')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        db_table = 'organizations'

    def __str__(self):
        return self.name


class VIPClient(models.Model):
    """VIP-клиент"""
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('inactive', 'Неактивный'),
        ('potential', 'Потенциальный'),
        ('archived', 'Архивный'),
    ]

    vip_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    position = models.CharField(max_length=200, verbose_name='Должность')
    phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    email = models.EmailField(max_length=100, verbose_name='Электронная почта')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Организация')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active', verbose_name='Статус')
    notes = models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')

    class Meta:
        verbose_name = 'VIP-клиент'
        verbose_name_plural = 'VIP-клиенты'
        db_table = 'vip_clients'

    def __str__(self):
        return self.full_name


class Interaction(models.Model):
    """Взаимодействие с VIP-клиентом"""
    TYPE_CHOICES = [
        ('meeting', 'Встреча'),
        ('email', 'Письмо'),
        ('call', 'Звонок'),
        ('project', 'Участие в проекте'),
        ('agreement', 'Согласование'),
        ('other', 'Другое'),
    ]

    CHANNEL_CHOICES = [
        ('phone', 'Телефон'),
        ('email', 'Email'),
        ('in_person', 'Личная встреча'),
        ('online', 'Онлайн'),
        ('other', 'Другое'),
    ]

    interaction_id = models.AutoField(primary_key=True)
    vip_client = models.ForeignKey(VIPClient, on_delete=models.CASCADE, verbose_name='VIP-клиент')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата взаимодействия')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Тип взаимодействия')
    channel = models.CharField(max_length=50, choices=CHANNEL_CHOICES, blank=True, null=True, verbose_name='Канал связи')
    description = models.TextField(verbose_name='Подробности взаимодействия')
    result = models.TextField(blank=True, null=True, verbose_name='Результат')

    class Meta:
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'
        db_table = 'interactions'
        ordering = ['-date']

    def __str__(self):
        return f"{self.vip_client.full_name} - {self.get_type_display()} ({self.date})"
