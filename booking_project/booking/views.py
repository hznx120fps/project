from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Room, Booking, Settings
from .forms import SettingsForm
from datetime import datetime


def is_admin(user):
    """Перевірка чи користувач адміністратор"""
    return user.is_staff or user.is_superuser


def room_list(request):
    """Отображение списка доступных комнат с фильтром по цветам"""
    rooms = Room.objects.all()

    selected_color = request.GET.get('color', '').strip()
    color_match_count = 0
    filtered_rooms = rooms

    if selected_color:
        filtered_rooms = rooms.filter(color__iexact=selected_color)
        color_match_count = filtered_rooms.count()
        filtered_rooms = filtered_rooms[:5]

    all_colors = Room.objects.values_list('color', flat=True).distinct().order_by('color')

    context = {
        'rooms': filtered_rooms,
        'all_colors': all_colors,
        'selected_color': selected_color,
        'color_match_count': color_match_count,
    }
    return render(request, 'booking/room_list.html', context)


def room_detail(request, room_id):
    """Детали комнаты и форма для бронирования"""
    room = get_object_or_404(Room, id=room_id)
    bookings = Booking.objects.filter(room=room, status__in=['confirmed', 'pending'])
    
    context = {
        'room': room,
        'bookings': bookings,
    }
    return render(request, 'booking/room_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def create_booking(request, room_id):
    """Создание бронирования"""
    room = get_object_or_404(Room, id=room_id)
    
    try:
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
        
        # Создание бронирования
        booking = Booking(
            user=request.user,
            room=room,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        
        # Проверка валидности
        booking.clean()
        booking.save()
        
        messages.success(request, f'✓ Номер "{room.name}" успішно забронювана!')
        return redirect('room_detail', room_id=room_id)
        
    except Exception as e:
        messages.error(request, f'✗ Помилка: {str(e)}')
        return redirect('room_detail', room_id=room_id)


def my_bookings(request):
    """Мои бронирования"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    """Отмена бронирования"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Бронювання відмінена')
    
    return redirect('my_bookings')


@login_required(login_url='login')
@user_passes_test(is_admin)
def settings_page(request):
    """Сторінка настроєк (тільки для адміністраторів)"""
    settings = Settings.get_settings()
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, '✓ Настройки успішно збережені!')
            return redirect('settings')
    else:
        form = SettingsForm(instance=settings)
    
    context = {
        'form': form,
        'settings': settings,
    }
    return render(request, 'booking/settings.html', context)
