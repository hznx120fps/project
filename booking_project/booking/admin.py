from django import forms
from django.contrib import admin
from django.forms.widgets import TextInput
from .models import Room, Booking, Settings


class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }


class SettingsAdminForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'
        widgets = {
            'background_color': TextInput(attrs={'type': 'color'}),
            'primary_color': TextInput(attrs={'type': 'color'}),
            'secondary_color': TextInput(attrs={'type': 'color'}),
            'text_color': TextInput(attrs={'type': 'color'}),
        }


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    list_display = ('name', 'capacity', 'price', 'color')
    search_fields = ('name',)
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'description', 'capacity', 'price')
        }),
        ('Дизайн', {
            'fields': ('color',),
            'description': 'Виберіть колір для кімнати'
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('user__username', 'room__name')


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    form = SettingsAdminForm
    list_display = ('__str__', 'primary_color', 'secondary_color')
    fieldsets = (
        ('Кольори', {
            'fields': ('background_color', 'primary_color', 'secondary_color', 'text_color')
        }),
        ('Інформація сайту', {
            'fields': ('site_title', 'site_description')
        }),
    )

    def has_add_permission(self, request):
        return self.model.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        return False
