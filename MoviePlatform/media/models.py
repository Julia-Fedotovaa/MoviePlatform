from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Q

from .validators import validate_rating, release_date_validator, validate_title
from django.db import models
from polymorphic.models import PolymorphicModel
from simple_history.models import HistoricalRecords


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название', validators=[validate_title])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название', validators=[validate_title])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class AbstractMedia(PolymorphicModel):
    title = models.CharField(max_length=100, verbose_name='Название', validators=[validate_title])
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

    @classmethod
    def get_movies_by_length_and_country(cls, max_length="02:00:00", exclude_country="USA"):
        """
        Получение фильмов, длина которых меньше указанной и страна не указана.
        """
        return cls.objects.select_related('country').filter(
            Q(length__lt=max_length) &
            ~Q(country__name=exclude_country) | Q(country=None)
        )

    def get_average_rating(self):
        return self.rating_set.aggregate(Avg('rating'))['rating__avg']

    def reviews(self):
        return self.rating_set.all()

    def __str__(self):
        return self.title + ' (' + str(self.release_date.year) + ')' + str([genre.name for genre in self.genres.all()])

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

    @classmethod
    def get_tvshows_by_seasons_count_and_country(cls, min_seasons_count=5, country='США'):
        """
        Получение сериалов с количеством сезонов больше указанного и страной.
        """
        return cls.objects.select_related('country').filter(
            Q(seasons_count__gt=min_seasons_count) &
            Q(country__name=country)
        )

    def get_average_rating(self):
        return self.rating_set.aggregate(Avg('rating'))['rating__avg']

    def get_media_type(self):
        return ContentType.objects.get_for_model(self)

    def reviews(self):
        return self.rating_set.all()

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

    @classmethod
    def get_ratings_by_media(cls, rating_range=(1, 2), country='США', title_contains='а'):
        """
        Получение медиа с оценкой вне указанного диапазона, страной и названием.
        """
        return cls.objects.select_related('media__country', 'media').filter(
            ~Q(rating__range=rating_range) &
            Q(media__country__name=country) &
            Q(media__title__icontains=title_contains)
        )

    def __str__(self):
        return f"{self.user} - {self.media} - {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
