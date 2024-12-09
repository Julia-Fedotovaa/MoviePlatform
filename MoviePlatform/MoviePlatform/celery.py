"""
Настройка Celery для проекта Django
"""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoviePlatform.settings')

app = Celery('MoviePlatform')

app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_url='redis://redis:6380',
    result_backend='redis://redis:6380',
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['tasks'])
