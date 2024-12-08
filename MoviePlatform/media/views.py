from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from media.models import Movie, TVShow, Country, Genre, Rating


class MediaView(TemplateView):
    template_name = 'media/media.html'
    context_object_name = 'media'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tvshows_list = cache.get('tvshows_list')
        if not tvshows_list:
            tvshows_list = TVShow.objects.all()
            cache.set('tvshows_list', tvshows_list, timeout=60 * 15)  # 15 минут

        movies_list = cache.get('movies_list')
        if not movies_list:
            movies_list = Movie.objects.all()
            cache.set('movies_list', movies_list, timeout=60 * 15)

        tvshows_paginator = Paginator(tvshows_list, 5)
        movies_paginator = Paginator(movies_list, 5)

        tvshows_page_number = self.request.GET.get('tvshows_page')
        movies_page_number = self.request.GET.get('movies_page')

        tvshows_page = tvshows_paginator.get_page(tvshows_page_number)
        movies_page = movies_paginator.get_page(movies_page_number)

        context['tvshows'] = tvshows_page
        context['movies'] = movies_page

        high_rated_movies = cache.get('high_rated_movies')
        if not high_rated_movies:
            high_rated_movies = list(Movie.get_high_rated()[0:3])
            cache.set('high_rated_movies', high_rated_movies, timeout=60 * 60)  # Кэширование на 1 час

        high_rated_tvshows = cache.get('high_rated_tvshows')
        if not high_rated_tvshows:
            high_rated_tvshows = list(TVShow.get_high_rated()[0:3])
            cache.set('high_rated_tvshows', high_rated_tvshows, timeout=60 * 60)

        context['high_rated_movies'] = high_rated_movies
        context['high_rated_tvshows'] = high_rated_tvshows

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
            self, *, object_list=..., **kwargs
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
