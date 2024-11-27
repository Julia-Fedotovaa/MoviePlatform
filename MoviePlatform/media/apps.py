from django.apps import AppConfig


class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media'
    verbose_name = 'Медиа'
    verbose_name_plural = 'Медиа'

    def ready(self):
        from . import signals
