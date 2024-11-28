from django.views.generic import ListView, TemplateView, DetailView

from media.models import Movie, TVShow


class MediaView(TemplateView):
    template_name = 'media/media.html'
    context_object_name = 'media'

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)

        # Добавляем список TVShow в контекст
        context['tvshows'] = TVShow.objects.all()
        context['movies'] = Movie.objects.all()
        context['high_rated_movies'] = Movie.get_high_rated()
        context['high_rated_tvshows'] = TVShow.get_high_rated()

        return context


class MovieView(DetailView):
    model = Movie
    template_name = 'media/movie.html'
    context_object_name = 'movie'