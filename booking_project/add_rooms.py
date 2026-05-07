import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
django.setup()

from booking.models import Room

# Данные для комнат с разными цветами
rooms_data = [
    {
        'name': 'Люкс - Синій',
        'description': 'Просторна люкс кімната з видом на море',
        'capacity': 2,
        'price': 150.00,
        'color': '#667eea'
    },
    {
        'name': 'Люкс - Червоний',
        'description': 'Класична люкс кімната з червоною декорацією',
        'capacity': 2,
        'price': 160.00,
        'color': '#e74c3c'
    },
    {
        'name': 'Люкс - Зелений',
        'description': 'Люкс кімната з природною зеленою стилізацією',
        'capacity': 2,
        'price': 155.00,
        'color': '#27ae60'
    },
    {
        'name': 'Стандарт - Жовтий',
        'description': 'Комфортна стандартна кімната з яскравим дизайном',
        'capacity': 1,
        'price': 80.00,
        'color': '#f39c12'
    },
    {
        'name': 'Стандарт - Фіолетовий',
        'description': 'Стандартна кімната з елегантним фіолетовим інтер\'єром',
        'capacity': 1,
        'price': 85.00,
        'color': '#9b59b6'
    },
    {
        'name': 'Стандарт - Рожевий',
        'description': 'Приватна стандартна кімната з м\'яким рожевим дизайном',
        'capacity': 1,
        'price': 75.00,
        'color': '#ff69b4'
    },
    {
        'name': 'Студія - Бірюзовий',
        'description': 'Компактна студія з сучасним бірюзовим оформленням',
        'capacity': 1,
        'price': 60.00,
        'color': '#1abc9c'
    },
    {
        'name': 'Студія - Помаранчевий',
        'description': 'Невелика уютна студія з теплим помаранчевим кольором',
        'capacity': 1,
        'price': 65.00,
        'color': '#ff7f50'
    },
    {
        'name': 'Студія - Сірий',
        'description': 'Мінімалістична студія в сірих тонах',
        'capacity': 1,
        'price': 55.00,
        'color': '#7f8c8d'
    },
    {
        'name': 'Люкс Сюіт - Глибокий Синій',
        'description': 'Преміум люкс сюіт з розкішним інтер\'єром',
        'capacity': 4,
        'price': 250.00,
        'color': '#2c3e50'
    },
    {
        'name': 'Люкс Сюіт - Золотистий',
        'description': 'Преміум сюіт з золотистим оформленням та люстрами',
        'capacity': 4,
        'price': 270.00,
        'color': '#f1c40f'
    },
    {
        'name': 'Сімейна - Зеленський Мох',
        'description': 'Великa кімната для сім\'ї з екологічним дизайном',
        'capacity': 4,
        'price': 200.00,
        'color': '#16a085'
    },
    {
        'name': 'Сімейна - Земля',
        'description': 'Просторна сімейна кімната з теплим коричневим дизайном',
        'capacity': 4,
        'price': 180.00,
        'color': '#8b4513'
    },
    {
        'name': 'VIP Penthouse - Електричний',
        'description': 'Екскlusивний VIP пентхаус на вищому поверсі',
        'capacity': 6,
        'price': 400.00,
        'color': '#3498db'
    },
    {
        'name': 'Конференц зал - Сланцевий',
        'description': 'Велика конференц-зала для зустрічей та заходів',
        'capacity': 50,
        'price': 500.00,
        'color': '#34495e'
    }
]

# Создание комнат
for room_data in rooms_data:
    room, created = Room.objects.get_or_create(
        name=room_data['name'],
        defaults={
            'description': room_data['description'],
            'capacity': room_data['capacity'],
            'price': room_data['price'],
            'color': room_data['color']
        }
    )
    if created:
        print(f"✓ Створено: {room.name} ({room.color})")
    else:
        print(f"→ Уже існує: {room.name}")

print(f"\n✅ Всього кімнат в базі: {Room.objects.count()}")
