"""Модуль для сигналов модели Country"""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Country


@receiver(post_migrate)
def populate_countries(sender, **kwargs):
    """Функция для заполнения модели Country"""
    if sender.name == 'media':
        countries = [
            'Австралия', 'Франция', 'США', 'Великобритания', 'Индия', 'Китай', 'Россия', 'Япония', 'Германия',
            'Италия', 'Испания', 'Канада', 'Южная Корея', 'Бразилия', 'Мексика', 'Турция', 'Швеция', 'Дания',
            'Норвегия', 'Финляндия', 'Бельгия', 'Голландия', 'Польша', 'Чехия', 'Словакия', 'Украина', 'Беларусь',
        ]

        if Country.objects.exists():
            return

        for country in countries:
            Country.objects.get_or_create(name=country)

        print('Модель Country заполнена')
