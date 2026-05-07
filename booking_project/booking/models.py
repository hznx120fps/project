from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    color = models.CharField(
        max_length=7,
        default='#667eea',
        help_text='Колір кімнати у форматі HEX (наприклад: #FF5733)'
    )

    def __str__(self):
        return self.name


class Settings(models.Model):
    """Глобальні настройки теми сайту"""
    # Кольори фону
    background_color = models.CharField(
        max_length=7,
        default='#ffffff',
        help_text='Колір фону сайту'
    )
    primary_color = models.CharField(
        max_length=7,
        default='#667eea',
        help_text='Основний колір (заголовки, кнопки)'
    )
    secondary_color = models.CharField(
        max_length=7,
        default='#764ba2',
        help_text='Вторинний колір (градієнти, акценти)'
    )
    text_color = models.CharField(
        max_length=7,
        default='#333333',
        help_text='Колір тексту'
    )
    
    # Параметри сайту
    site_title = models.CharField(
        max_length=200,
        default='Система бронювання кімнат',
        help_text='Назва сайту'
    )
    site_description = models.TextField(
        default='Зручна система бронювання номерів готелю',
        help_text='Опис сайту'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Настройки сайту'
        verbose_name_plural = 'Настройки сайту'
    
    def __str__(self):
        return 'Глобальні настройки'
    
    @classmethod
    def get_settings(cls):
        """Отримати або створити настройки за замовчуванням"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікування'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Відмінено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        # 1. Проверка: дата окончания позже начала
        if self.start_date >= self.end_date:
            raise ValidationError("Дата окончания должна быть позже даты начала")

        # 2. Проверка: нет ли пересечения бронирований
        overlapping = Booking.objects.filter(
            room=self.room,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("Эта комната уже забронирована на выбранное время")

    def __str__(self):
        return f"{self.room} | {self.start_date}"