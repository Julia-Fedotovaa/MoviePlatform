"""Модели приложения media"""
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Avg, Q
from django.urls.base import reverse
from django.utils import timezone

from .validators import validate_rating, release_date_validator, validate_title
from django.db import models
from polymorphic.models import PolymorphicModel
from simple_history.models import HistoricalRecords

MEDIA_TYPE_CHOICES = [
    ('movie', 'Movie'),
    ('tvshow', 'TV Show'),
]


class MediaManager(models.Manager):
    def top_rated(self):
        return self.filter(rating__gte=3).order_by('-rating')


class Genre(models.Model):
    """Модель для жанра"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название', validators=[validate_title])

    def __str__(self):
        """Строковое представление объекта"""
        return self.name

    class Meta:
        """Метаданные модели"""
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Country(models.Model):
    """Модель для страны"""
    name = models.CharField(max_length=30, unique=True, verbose_name='Название', validators=[validate_title])

    def __str__(self):
        """Строковое представление объекта"""
        return self.name

    class Meta:
        """Метаданные модели"""
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']


class Media(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField(default=timezone.now)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="media")
    genres = models.ManyToManyField(Genre, through='MediaGenre')
    type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    poster = models.ImageField(upload_to='media_posters/', blank=True, null=True)
    rating = models.IntegerField(default=0, validators=[validate_rating], blank=True, null=True)
    file = models.FileField(upload_to='media_files/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    objects = MediaManager()

    class Meta:
        ordering = ['-release_date']
        verbose_name = 'Другое медиа'
        verbose_name_plural = 'Другие медиа'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('media_detail', args=[str(self.id)])

    def clean_rating(self):
        if self.rating < 0 or self.rating > 10:
            raise ValidationError("Rating must be between 0 and 10")
        return self.rating

    def save(self, *args, **kwargs):
        # Дополнительная логика перед сохранением
        if not self.release_date:
            self.release_date = timezone.now()

        # Сохраняем объект в базу данных
        super(Media, self).save(*args, **kwargs)


class MediaGenre(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    date_added = models.DateField(default=timezone.now)


class AbstractMedia(PolymorphicModel):
    """Абстрактная модель для медиа"""
    title = models.CharField(max_length=100, verbose_name='Название', validators=[validate_title])
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='posters/', verbose_name='Постер')
    release_date = models.DateField(verbose_name='Дата выхода', validators=[release_date_validator])
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)

    def __str__(self):
        """Строковое представление объекта"""
        return self.title

    def get_media_type(self):
        """Метод для получения типа медиа"""
        return ContentType.objects.get_for_model(self)

    class Meta:
        """Метаданные модели"""
        verbose_name = 'Медиа'
        verbose_name_plural = 'Медиа'


class Movie(AbstractMedia):
    """Модель для фильма"""
    history = HistoricalRecords()
    length = models.TimeField(verbose_name='Продолжительность')

    def get_media_type(self):
        """Метод для получения типа медиа"""
        return 'movie'

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
        """Метод для получения среднего рейтинга"""
        return self.rating_set.aggregate(Avg('rating'))['rating__avg']

    def reviews(self):
        """Метод для получения отзывов"""
        return self.rating_set.all()

    def __str__(self):
        """Строковое представление объекта"""
        return self.title + ' (' + str(self.release_date.year) + ')' + str([genre.name for genre in self.genres.all()])

    class Meta:
        """Метаданные модели"""
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class TVShow(AbstractMedia):
    """Модель для сериала"""
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
        """Метод для получения среднего рейтинга"""
        return self.rating_set.aggregate(Avg('rating'))['rating__avg']

    def get_media_type(self):
        """Метод для получения типа медиа"""
        return 'tvshow'

    def reviews(self):
        """Метод для получения отзывов"""
        return self.rating_set.all()

    def __str__(self):
        """Строковое представление объекта"""
        return self.title

    class Meta:
        """Метаданные модели"""
        verbose_name = 'Сериал'
        verbose_name_plural = 'Сериалы'


class Rating(models.Model):
    """Модель для рейтинга"""
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
        """Строковое представление объекта"""
        return f"{self.user} - {self.media} - {self.rating}"

    class Meta:
        """Метаданные модели"""
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
