from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from simple_history.admin import SimpleHistoryAdmin

from .models import Country, Genre, Movie, TVShow, Rating

class MovieResource(resources.ModelResource):
    def get_export_queryset(self, queryset):
        return queryset.filter(is_published=True)

    def dehydrate_title(self, movie):
        return f"Фильм: {movie.title}"

    def dehydrate_release_date(self, movie):
        return movie.release_date.strftime('%d-%m-%Y')

    def get_genres(self, movie):
        return ", ".join(genre.name for genre in movie.genres.all())

@admin.register(Movie)
class MovieAdmin(ExportMixin, SimpleHistoryAdmin):
    list_display = ('title', 'release_date', 'country', 'length', 'get_genres')
    list_filter = ('country', 'genres')
    search_fields = ('title', 'country')
    ordering = ('title', 'release_date')

    def get_genres(self, obj):
        return ", ".join(genre.name for genre in obj.genres.all())

    get_genres.short_description = 'Жанры'


class TVShowResource(resources.ModelResource):
    fields = ('title', 'release_date', 'country', 'seasons_count', 'get_genres')

    def get_export_queryset(self, queryset):
        return queryset.filter(seasons_count__gt=3)

    def dehydrate_title(self, tvshow):
        return f"Сериал: {tvshow.title}"

    def dehydrate_release_date(self, tvshow):
        return tvshow.release_date.strftime('%d-%m-%Y')

    def get_genres(self, tvshow):
        return ", ".join(genre.name for genre in tvshow.genres.all())

@admin.register(TVShow)
class TVShowAdmin(ExportMixin, SimpleHistoryAdmin):
    list_display = ('title', 'release_date', 'country', 'seasons_count')
    list_filter = ('country', 'genres')
    search_fields = ('title', 'country')
    ordering = ('title', 'release_date')


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
