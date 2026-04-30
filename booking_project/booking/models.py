from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


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