from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Room, Booking
from datetime import datetime


def room_list(request):
    """Отображение списка доступных комнат"""
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})


def room_detail(request, room_id):
    """Детали комнаты и форма для бронирования"""
    room = get_object_or_404(Room, id=room_id)
    bookings = Booking.objects.filter(room=room, status__in=['confirmed', 'pending'])
    
    context = {
        'room': room,
        'bookings': bookings,
    }
    return render(request, 'booking/room_detail.html', context)


@login_required(login_url='admin:login')
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
        return redirect('admin:login')
    
    bookings = Booking.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required(login_url='admin:login')
def cancel_booking(request, booking_id):
    """Отмена бронирования"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Бронювання відмінена')
    
    return redirect('my_bookings')
