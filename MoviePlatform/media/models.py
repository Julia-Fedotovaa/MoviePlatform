from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

from .validators import validate_rating, release_date_validator
from django.db import models
from polymorphic.models import PolymorphicModel
from simple_history.models import HistoricalRecords


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


class AbstractMedia(PolymorphicModel):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='posters/', verbose_name='Постер')
    release_date = models.DateField(verbose_name='Дата выхода', validators=[release_date_validator])
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Медиа'
        verbose_name_plural = 'Медиа'


class Movie(AbstractMedia):
    history = HistoricalRecords()
    length = models.TimeField(verbose_name='Продолжительность')

    def get_media_type(self):
        return ContentType.objects.get_for_model(self)

    @classmethod
    def get_high_rated(cls, threshold=4.0):
        """
        Получение фильмов с высоким средним рейтингом.
        """
        return cls.objects.annotate(
            average_rating=Avg('abstractmedia_ptr__rating__rating')
        ).filter(average_rating__gt=threshold)

    def __str__(self):
        return self.title + ' (' + str(self.release_date.year) + ')'

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class TVShow(AbstractMedia):
    history = HistoricalRecords()
    seasons_count = models.PositiveIntegerField(verbose_name='Количество сезонов')

    @classmethod
    def get_high_rated(cls, threshold=4.0):
        """
        Получение сериалов с высоким средним рейтингом.
        """
        return cls.objects.annotate(
            average_rating=Avg('abstractmedia_ptr__rating__rating')
        ).filter(average_rating__gt=threshold)

    def get_media_type(self):
        return ContentType.objects.get_for_model(self)

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
    rating = models.PositiveIntegerField(verbose_name='Оценка', default=5, validators=[validate_rating])

    media = models.ForeignKey(
        AbstractMedia, on_delete=models.CASCADE,
        verbose_name='Медиа',
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.user} - {self.media} - {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
