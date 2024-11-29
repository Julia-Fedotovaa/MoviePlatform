from import_export import resources

from media.models import TVShow, Movie


class MovieResource(resources.ModelResource):
    class Meta:
        model = Movie
        fields = ('Заголовок', 'Дата выхода', 'Жанры', 'Страна', 'Продолжительность')

    def get_export_queryset(self, queryset):
        return queryset.filter(is_published=True)

    def dehydrate_title(self, movie):
        return f"Фильм: {movie.title}"

    def dehydrate_release_date(self, movie):
        return movie.release_date.strftime('%d-%m-%Y')

    def dehydrate_genres(self, movie):
        return ", ".join(genre.name for genre in movie.genres.all())

    def dehydrate_country(self, movie):
        return movie.country.name

    def dehydrate_length(self, movie):
        return movie.length.strftime('%H:%M')


class TVShowResource(resources.ModelResource):
    class Meta:
        model = TVShow
        fields = ('title', 'release_date', 'genres', 'country', 'seasons_count')

    def get_export_queryset(self, queryset):
        return queryset.filter(seasons_count__gt=6)

    def dehydrate_title(self, tvshow):
        return f"Сериал: {tvshow.title}"

    def dehydrate_release_date(self, tvshow):
        return tvshow.release_date.strftime('%d-%m-%Y')

    def dehydrate_genres(self, tvshow):
        return ", ".join(genre.name for genre in tvshow.genres.all())

    def dehydrate_country(self, tvshow):
        return tvshow.country.name

    def dehydrate_seasons_count(self, tvshow):
        return self.get_seasons_count(tvshow)

    def get_seasons_count(self, tvshow):
        return tvshow.seasons_count
