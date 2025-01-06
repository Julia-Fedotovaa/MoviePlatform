"""Модуль административной панели приложения media"""
from io import BytesIO

from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple, DateInput
from django.http import HttpResponse
from import_export.admin import ExportMixin
from import_export.formats.base_formats import JSON, CSV, XLSX
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from simple_history.admin import SimpleHistoryAdmin

from .models import Country, Genre, Movie, TVShow, Rating, Media, MediaGenre
from .resources import MovieResource, TVShowResource

app_name = 'Медиа'


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1


@admin.register(Movie)
class MovieAdmin(ExportMixin, SimpleHistoryAdmin):
    """
    Административная панель для моделей приложения media
    """
    list_display = ('title', 'release_date', 'country', 'length', 'get_genres')
    list_filter = ('country', 'genres')
    search_fields = ('title', 'country')
    ordering = ('title', 'release_date')
    resource_class = MovieResource
    formats = (JSON, CSV, XLSX)
    inlines = [RatingInline]

    def get_genres(self, obj):
        """Получение жанров фильма"""
        return ", ".join(genre.name for genre in obj.genres.all())

    get_genres.short_description = 'Жанры'


@admin.register(TVShow)
class TVShowAdmin(ExportMixin, SimpleHistoryAdmin):
    """Административная панель для модели TVShow"""
    list_display = ('title', 'release_date', 'country', 'seasons_count')
    list_filter = ('country', 'genres')
    search_fields = ('title', 'country')
    ordering = ('title', 'release_date')
    resource_class = TVShowResource
    formats = (JSON, CSV, XLSX)
    inlines = [RatingInline]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Административная панель для модели Rating"""
    list_display = ('user', 'get_media_object', 'rating')
    list_filter = ('rating',)
    search_fields = ('user', 'media__title')
    ordering = ('user', 'rating')

    def get_media_object(self, obj):
        """Получение медиа объекта"""
        return str(obj.media) if obj.media else "Не задано"

    get_media_object.short_description = 'Медиа'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Административная панель для модели Country"""
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Административная панель для модели Genre"""
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Административная панель для модели Media"""
    list_display = ('title', 'release_date', 'country', 'get_genres')
    list_filter = ('country', 'genres')
    search_fields = ('title', 'country')
    ordering = ('title', 'release_date')

    def get_genres(self, obj):
        """Получение жанров медиа"""
        return ", ".join(genre.name for genre in obj.genres.all())

    get_genres.short_description = 'Жанры'

    def generate_pdf(self, request, queryset):
        """Метод для генерации PDF для каждого объекта"""
        for media in queryset:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={media.title}.pdf'

            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))
            p.setFont('DejaVuSans', 12)
            p.drawString(100, 750, f'Title: {media.title}')
            p.drawString(100, 730, f'Release Date: {media.release_date}')
            p.drawString(100, 710, f'Country: {media.country.name}')
            p.drawString(100, 690, f'Genres: {", ".join(genre.name for genre in media.genres.all())}')
            p.showPage()
            p.save()

            buffer.seek(0)
            response.write(buffer.read())
            return response

    generate_pdf.short_description = 'Generate PDF for selected Media'

    actions = [generate_pdf]


@admin.register(MediaGenre)
class MediaGenreAdmin(admin.ModelAdmin):
    """Административная панель для модели MediaGenre"""
    list_display = ('media', 'genre')
    list_filter = ('genre',)
    search_fields = ('media', 'genre')
    ordering = ('media', 'genre')
    formfield_overrides = {
        models.DateField: {'widget': DateInput(attrs={'type': 'date'})},
    }
