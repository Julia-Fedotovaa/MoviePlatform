"""Модуль для ресурсов экспорта моделей"""
from import_export import resources

from media.models import TVShow, Movie


class MovieResource(resources.ModelResource):
    """Ресурс для экспорта модели Movie"""
    class Meta:
        """Метаданные ресурса"""
        model = Movie
        fields = ('Заголовок', 'Дата выхода', 'Жанры', 'Страна', 'Продолжительность')

    def get_export_queryset(self, queryset):
        """Метод для получения экспортируемого запроса"""
        return queryset.filter(is_published=True)

    def dehydrate_title(self, movie):
        """Метод для получения заголовка фильма"""
        return f"Фильм: {movie.title}"

    def dehydrate_release_date(self, movie):
        """Метод для получения даты выхода фильма"""
        return movie.release_date.strftime('%d-%m-%Y')

    def dehydrate_genres(self, movie):
        """Метод для получения жанров фильма"""
        return ", ".join(genre.name for genre in movie.genres.all())

    def dehydrate_country(self, movie):
        """Метод для получения страны фильма"""
        return movie.country.name

    def dehydrate_length(self, movie):
        """Метод для получения продолжительности фильма"""
        return movie.length.strftime('%H:%M')


class TVShowResource(resources.ModelResource):
    """Ресурс для экспорта модели TVShow"""
    class Meta:
        """Метаданные ресурса"""
        model = TVShow
        fields = ('title', 'release_date', 'genres', 'country', 'seasons_count')

    def get_export_queryset(self, queryset):
        """Метод для получения экспортируемого запроса"""
        return queryset.filter(seasons_count__gt=6)

    def dehydrate_title(self, tvshow):
        """Метод для получения заголовка сериала"""
        return f"Сериал: {tvshow.title}"

    def dehydrate_release_date(self, tvshow):
        """Метод для получения даты выхода сериала"""
        return tvshow.release_date.strftime('%d-%m-%Y')

    def dehydrate_genres(self, tvshow):
        """Метод для получения жанров сериала"""
        return ", ".join(genre.name for genre in tvshow.genres.all())

    def dehydrate_country(self, tvshow):
        """Метод для получения страны сериала"""
        return tvshow.country.name

    def dehydrate_seasons_count(self, tvshow):
        """Метод для получения количества сезонов сериала"""
        return self.get_seasons_count(tvshow)

    def get_seasons_count(self, tvshow):
        """Метод для получения количества сезонов сериала"""
        return tvshow.seasons_count
