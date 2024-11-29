from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from media.models import Movie, TVShow, Country, Genre, Rating


class MediaView(TemplateView):
    template_name = 'media/media.html'
    context_object_name = 'media'

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)

        # Получаем все ТВ-шоу и фильмы
        tvshows_list = TVShow.objects.all()
        movies_list = Movie.objects.all()

        # Создаем пагинаторы
        tvshows_paginator = Paginator(tvshows_list, 5)  # 10 объектов на странице
        movies_paginator = Paginator(movies_list, 5)  # 10 объектов на странице

        # Получаем номер текущей страницы
        tvshows_page_number = self.request.GET.get('tvshows_page')
        movies_page_number = self.request.GET.get('movies_page')

        # Получаем объекты для текущей страницы
        tvshows_page = tvshows_paginator.get_page(tvshows_page_number)
        movies_page = movies_paginator.get_page(movies_page_number)

        # Добавляем пагинированные объекты в контекст
        context['tvshows'] = tvshows_page
        context['movies'] = movies_page
        context['high_rated_movies'] = Movie.get_high_rated()[0:3]
        context['high_rated_tvshows'] = TVShow.get_high_rated()[0:3]

        return context


class MovieView(DetailView):
    model = Movie
    template_name = 'media/movie.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Movie.reviews(self.object)
        for review in reviews:
            review.full_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)

        context['reviews'] = reviews

        print([review.full_stars for review in reviews])

        return context

    def post(self, request, *args, **kwargs):
        movie = self.get_object()
        rating = request.POST.get('rating')

        if rating and 1 <= int(rating) <= 5:
            Rating.objects.create(
                media=movie,
                user=request.user,
                rating=int(rating),
            )

        return redirect('movie', pk=movie.pk)


class TVShowView(DetailView):
    model = TVShow
    template_name = 'media/tvshow.html'
    context_object_name = 'tvshow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = TVShow.reviews(self.object)
        for review in reviews:
            review.full_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)

        context['reviews'] = reviews

        print([review.full_stars for review in reviews])

        return context

    def post(self, request, *args, **kwargs):
        tvshow = self.get_object()
        rating = request.POST.get('rating')

        if rating and 1 <= int(rating) <= 5:
            Rating.objects.create(
                media=tvshow,
                user=request.user,
                rating=int(rating),
            )

        return redirect('tvshow', pk=tvshow.pk)


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


class ComplexQueriesView(TemplateView):
    template_name = 'media/complex_queries.html'
    context_object_name = 'tvshows'

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)

        context['tvshows'] = TVShow.get_tvshows_by_seasons_count_and_country()
        context['movies'] = Movie.get_movies_by_length_and_country()
        context['reviews'] = Rating.get_ratings_by_media()

        for review in context['reviews']:
            review.full_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)
            review.media_name = review.media.title

        return context