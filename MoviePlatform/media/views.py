from django.views.generic import ListView, TemplateView, DetailView, CreateView

from media.models import Movie, TVShow, Country, Genre


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


class TVShowView(DetailView):
    model = TVShow
    template_name = 'media/tvshow.html'
    context_object_name = 'tvshow'


class AddMovieView(CreateView):
    model = Movie
    template_name = 'media/add_movie.html'
    fields = ['title', 'description', 'poster', 'release_date', 'length', 'genres', 'country']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['genres'] = Genre.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print(self.request.POST)
        return super().form_valid(form)


class AddTVShowView(CreateView):
    model = TVShow
    template_name = 'media/add_tvshow.html'
    fields = ['title', 'description', 'poster', 'release_date', 'seasons_count', 'genres', 'country']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['genres'] = Genre.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print(self.request.POST)
        return super().form_valid(form)