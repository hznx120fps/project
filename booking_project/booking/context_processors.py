from .models import Settings


def settings_context(request):
    """Context processor для передачи настроек у всі шаблони"""
    settings = Settings.get_settings()
    return {
        'settings': settings
    }
