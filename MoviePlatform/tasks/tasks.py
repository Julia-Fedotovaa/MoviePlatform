"""Модуль задач Celery"""
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

from media.models import Movie, TVShow, Rating


@shared_task
def send_high_rated_media_to_users():
    """Отправка списка медиа с высоким рейтингом"""
    threshold = 4.0
    movies = Movie.get_high_rated(threshold)
    tvshows = TVShow.get_high_rated(threshold)
    print('aaaaaa')

    if movies.exists() or tvshows.exists():
        message = "Рекомендуем посмотреть:\n\n"

        if movies.exists():
            message += "Фильмы:\n"
            for movie in movies:
                message += f"- {movie.title} ({movie.release_date.year})\n"

        if tvshows.exists():
            message += "\nСериалы:\n"
            for show in tvshows:
                message += f"- {show.title} ({show.release_date.year})\n"

        send_mail(
            'Ваши рекомендации на неделю',
            message,
            'noreply@movieplatform.com',
            [user.email for user in User.objects.all() if user.email and user.email != ''],
            fail_silently=False,
        )

    return f"Отправлены рекомендации: {movies.count()} фильмов и {tvshows.count()} сериалов."


@shared_task
def clean_empty_ratings():
    """Удаление рейтингов без связанного медиа"""
    deleted_count, _ = Rating.objects.filter(media__isnull=True).delete()
    return f"Удалено {deleted_count} записей без медиа."
