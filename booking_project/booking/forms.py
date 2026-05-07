from django import forms
from .models import Settings


class SettingsForm(forms.ModelForm):
    background_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'color-picker'
        }),
        label='Колір фону'
    )
    primary_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'color-picker'
        }),
        label='Основний колір'
    )
    secondary_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'color-picker'
        }),
        label='Вторинний колір'
    )
    text_color = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'color-picker'
        }),
        label='Колір тексту'
    )
    site_title = forms.CharField(
        max_length=200,
        label='Назва сайту',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    site_description = forms.CharField(
        label='Опис сайту',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )
    
    class Meta:
        model = Settings
        fields = ['background_color', 'primary_color', 'secondary_color', 'text_color', 'site_title', 'site_description']
