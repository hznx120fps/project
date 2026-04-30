import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
django.setup()

from django.contrib.auth.models import User
from booking.models import Room, Booking

# Видалю старого адміна якщо існує
User.objects.filter(username='admin').delete()

# Створю суперкористувача
admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
print(f"✓ Суперкористувач створений: admin / admin123")

# Видалю старі номери
Room.objects.all().delete()

# Створю тестові номери
rooms_data = [
    {
        'name': 'Люкс з видом на море',
        'description': 'Комфортний номер з панорамним видом на море, балконом та сучасним дизайном',
        'capacity': 2,
        'price': 2500.00
    },
    {
        'name': 'Двомісна стандарт',
        'description': 'Затишна кімната з двоспальним ліжком, телевізором та ванною кімнатою',
        'capacity': 2,
        'price': 1500.00
    },
    {
        'name': 'Сімейна на 4 осіб',
        'description': 'Просторна кімната з двома спальнями, ідеальна для родин',
        'capacity': 4,
        'price': 2000.00
    },
    {
        'name': 'Одномісна економ',
        'description': 'Компактна кімната з односпальним ліжком, все необхідне',
        'capacity': 1,
        'price': 800.00
    },
    {
        'name': 'Люкс преміум',
        'description': 'Розкішна кімната з джакузі, міні-баром та VIP сервісом',
        'capacity': 2,
        'price': 4500.00
    }
]

for room_data in rooms_data:
    room = Room.objects.create(**room_data)
    print(f"✓ Створений номер: {room.name} ({room.price}₴/ніч)")

print("\n✓ Ініціалізація БД завершена!")
print("\nДані для входу в панель адміністратора:")
print("Користувач: admin")
print("Пароль: admin123")
