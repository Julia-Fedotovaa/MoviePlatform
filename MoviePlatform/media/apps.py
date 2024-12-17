"""Модуль приложения медиа"""
from django.apps import AppConfig


class MediaConfig(AppConfig):
    """Конфигурация приложения медиа"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media'
    verbose_name = 'Медиа'
    verbose_name_plural = 'Медиа'

    def ready(self):
        """Импорт сигналов"""
        from . import signals
