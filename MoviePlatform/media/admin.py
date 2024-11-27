from django.contrib import admin
from import_export.admin import ExportMixin
from simple_history.admin import SimpleHistoryAdmin

from .models import Country, Genre, Movie, TVShow, Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_media_object', 'rating')
    list_filter = ('rating',)
    search_fields = ('user', 'media__title')
    ordering = ('user', 'rating')

    def get_media_object(self, obj):
        return str(obj.media) if obj.media else "Не задано"

    get_media_object.short_description = 'Медиа'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Movie)
class MovieAdmin(ExportMixin, SimpleHistoryAdmin):
    list_display = ('title', 'release_date', 'country', 'length', 'get_genres')
    list_filter = ('country', 'genres')
    search_fields = ('title', 'country')
    ordering = ('title', 'release_date')

    def get_genres(self, obj):
        return ", ".join(genre.name for genre in obj.genres.all())

    get_genres.short_description = 'Жанры'


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'country', 'seasons_count')
    list_filter = ('country', 'genres')
    search_fields = ('title', 'country')
    ordering = ('title', 'release_date')
