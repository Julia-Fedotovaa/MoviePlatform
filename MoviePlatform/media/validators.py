"""Модуль с валидаторами для полей моделей"""
from datetime import date

from rest_framework.exceptions import ValidationError

def validate_title(value):
    """Валидатор для названия фильма или сериала"""
    if len(value) < 2:
        raise ValidationError("Название должно содержать не менее 2 символов.")

    return value


def validate_rating(value):
    """Валидатор для рейтинга"""
    if value < 1 or value > 5:
        raise ValidationError("Рейтинг должен быть в диапазоне от 1 до 5.")

    return value


def release_date_validator(value):
    """Валидатор для даты выхода фильма или сериала"""
    if value > date.today():
        raise ValidationError("Дата выхода не может быть в будущем.")

    if value < date(1900, 1, 1):
        raise ValidationError("Дата выхода не может быть раньше 1900 года.")

    return value
