from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class AbstractMedia(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='posters/', verbose_name='Постер')
    release_date = models.DateField(verbose_name='Дата выхода')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')

    class Meta:
        abstract = True


class Movie(AbstractMedia):
    length = models.TimeField(verbose_name='Продолжительность')

    def __str__(self):
        return self.title + ' (' + str(self.release_date.year) + ')'

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class TVShow(AbstractMedia):
    seasons_count = models.PositiveIntegerField(verbose_name='Количество сезонов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сериал'
        verbose_name_plural = 'Сериалы'


class Rating(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    rating = models.PositiveIntegerField(verbose_name='Оценка', default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    media = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user} - {self.media} - {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'