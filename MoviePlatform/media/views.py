"""Модуль представлений приложения media"""
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from media.forms import MediaForm
from media.models import Movie, TVShow, Country, Genre, Rating, Media, AbstractMedia


def media_list_view(request):
    # chaining filters
    media_list = Media.objects.prefetch_related('genres').filter(rating__gte=1).order_by('-release_date')

    paginator = Paginator(media_list, 5)
    page = request.GET.get('page')

    try:
        media = paginator.page(page)
    except PageNotAnInteger:
        media = paginator.page(1)
    except EmptyPage:
        media = paginator.page(paginator.num_pages)

    media_titles = media_list.values_list('title', flat=True)
    has_high_rated = media_list.filter(rating__gte=4).exists()

    return render(request, 'media_list.html',
                  {'media': media,
                   'media_titles': media_titles,
                   'has_high_rated': has_high_rated
                   })


def media_detail_view(request, pk):
    media = get_object_or_404(Media, pk=pk)
    return render(request, 'media_detail.html', {'media': media})


class MediaView(TemplateView):
    """Представление для отображения списка фильмов и сериалов"""
    template_name = 'media/media.html'
    context_object_name = 'media'

    def get_context_data(self, **kwargs):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('search', '').strip()

        tvshows_list = cache.get('tvshows_list')
        if not tvshows_list:
            tvshows_list = TVShow.objects.all()
            cache.set('tvshows_list', tvshows_list, timeout=60 * 15)  # 15 минут
        else:
            tvshows_list = TVShow.objects.filter(id__in=[tvshow.id for tvshow in tvshows_list])

        movies_list = cache.get('movies_list')
        if not movies_list:
            movies_list = Movie.objects.all()
            cache.set('movies_list', movies_list, timeout=60 * 15)
        else:
            movies_list = Movie.objects.filter(id__in=[movie.id for movie in movies_list])

        tvshows_list = tvshows_list.distinct()
        movies_list = movies_list.distinct()

        tvshows_list = tvshows_list.exclude(is_published=False)
        movies_list = movies_list.exclude(is_published=False)

        if search_query:
            tvshows_list = tvshows_list.filter(title__icontains=search_query)
            movies_list = movies_list.filter(title__icontains=search_query)

        tvshows_paginator = Paginator(tvshows_list, 5)
        movies_paginator = Paginator(movies_list, 5)

        tvshows_page_number = self.request.GET.get('tvshows_page')
        movies_page_number = self.request.GET.get('movies_page')

        tvshows_page = tvshows_paginator.get_page(tvshows_page_number)
        movies_page = movies_paginator.get_page(movies_page_number)

        context['tvshows'] = tvshows_page
        context['movies'] = movies_page

        high_rated_movies = Movie.get_high_rated()[0:3]
        high_rated_tvshows = TVShow.get_high_rated()[0:3]

        movie_count = Movie.objects.aggregate(total=Count('id'))['total']
        context['movie_count'] = movie_count

        tvshow_count = TVShow.objects.aggregate(total=Count('id'))['total']
        context['tvshow_count'] = tvshow_count

        context['high_rated_movies'] = high_rated_movies
        context['high_rated_tvshows'] = high_rated_tvshows

        return context


class MovieView(DetailView):
    """Представление для отображения информации о фильме"""
    model = Movie
    template_name = 'media/movie.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)
        reviews = Movie.reviews(self.object)
        for review in reviews:
            review.full_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)

        context['reviews'] = reviews

        print([review.full_stars for review in reviews])

        return context

    def post(self, request, *args, **kwargs):
        """Метод для добавления рейтинга к фильму"""
        movie = self.get_object()
        rating = request.POST.get('rating')

        if rating and 1 <= int(rating) <= 5:
            Rating.objects.create(
                media=movie,
                user=request.user,
                rating=int(rating),
            )

        request.session['last_viewed_movie'] = movie.pk

        return redirect('movie', pk=movie.pk)


class TVShowView(DetailView):
    """Представление для отображения информации о сериале"""
    model = TVShow
    template_name = 'media/tvshow.html'
    context_object_name = 'tvshow'

    def get_context_data(self, **kwargs):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)
        reviews = TVShow.reviews(self.object)
        for review in reviews:
            review.full_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)

        context['reviews'] = reviews

        print([review.full_stars for review in reviews])

        return context

    def post(self, request, *args, **kwargs):
        """Метод для добавления рейтинга к сериалу"""
        tvshow = self.get_object()
        rating = request.POST.get('rating')

        if rating and 1 <= int(rating) <= 5:
            Rating.objects.create(
                media=tvshow,
                user=request.user,
                rating=int(rating),
            )

        request.session['last_viewed_tvshow'] = tvshow.pk

        return redirect('tvshow', pk=tvshow.pk)


class ReviewEditView(TemplateView):
    """Представление для редактирования отзыва"""
    template_name = 'media/review_edit.html'

    media_type = None
    media_id = None

    def get_context_data(self, **kwargs):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)
        media_id = self.kwargs.get('pk')
        rating_id = self.kwargs.get('rating')

        context['media'] = get_object_or_404(Movie, pk=media_id)
        if not context['media']:
            context['media'] = get_object_or_404(TVShow, pk=media_id)
            if not context['media']:
                raise ValueError('Media not found')

        self.media_type = context['media'].get_media_type()
        self.media_id = media_id
        context['rating'] = Rating.objects.get(pk=rating_id)
        if context['rating'].media.id != int(media_id):
            raise ValueError('Rating not found')

        return context

    def post(self, request, *args, **kwargs):
        """Метод для обновления рейтинга"""
        rating = Rating.objects.get(pk=self.kwargs.get('rating'))
        rating.rating = request.POST.get('rating')
        rating.save()
        media = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        if not media:
            media = get_object_or_404(TVShow, pk=self.kwargs.get('pk'))
            if not media:
                raise ValueError('Media not found')

        media_type = media.get_media_type()

        if media_type == 'movie':
            return redirect('movie', pk=media.id)
        elif media_type == 'tvshow':
            return redirect('tvshow', pk=media.id)


class ReviewDeleteView(TemplateView):
    """Представление для удаления отзыва"""
    template_name = 'media/review_delete.html'

    media_type = None
    media_id = None

    def get_context_data(self, **kwargs):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)
        media_id = self.kwargs.get('pk')
        rating_id = self.kwargs.get('rating')

        context['media'] = get_object_or_404(Movie, pk=media_id)
        if not context['media']:
            context['media'] = get_object_or_404(TVShow, pk=media_id)
            if not context['media']:
                raise ValueError('Media not found')

        self.media_type = context['media'].get_media_type()
        self.media_id = media_id
        context['rating'] = Rating.objects.get(pk=rating_id)
        if context['rating'].media.id != int(media_id):
            raise ValueError('Rating not found')

        return context

    def post(self, request, *args, **kwargs):
        """Метод для удаления рейтинга"""
        rating = Rating.objects.get(pk=self.kwargs.get('rating'))
        media = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        if not media:
            media = get_object_or_404(TVShow, pk=self.kwargs.get('pk'))
            if not media:
                raise ValueError('Media not found')

        media_type = media.get_media_type()

        rating.delete()

        if media_type == 'movie':
            return redirect('movie', pk=media.id)
        elif media_type == 'tvshow':
            return redirect('tvshow', pk=media.id)


class AddMovieView(CreateView):
    """Представление для добавления фильма"""
    model = Movie
    template_name = 'media/add_movie.html'
    fields = ['title', 'description', 'poster', 'release_date', 'length', 'genres', 'country']
    success_url = '/'

    def get_context_data(self, **kwargs):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['genres'] = Genre.objects.all()
        return context

    def form_valid(self, form):
        new_movie = form.save(commit=False)
        new_movie.save()
        return super().form_valid(form)


class AddTVShowView(CreateView):
    """Представление для добавления сериала"""
    model = TVShow
    template_name = 'media/add_tvshow.html'
    fields = ['title', 'description', 'poster', 'release_date', 'seasons_count', 'genres', 'country']
    success_url = '/'

    def get_context_data(self, **kwargs):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['genres'] = Genre.objects.all()
        return context


class ComplexQueriesView(TemplateView):
    """Представление для отображения сложных запросов"""
    template_name = 'media/complex_queries.html'
    context_object_name = 'tvshows'

    def get_context_data(
            self, *, object_list=..., **kwargs
    ):
        """Метод для получения контекста"""
        context = super().get_context_data(**kwargs)

        context['tvshows'] = TVShow.get_tvshows_by_seasons_count_and_country()
        context['movies'] = Movie.get_movies_by_length_and_country()
        context['reviews'] = Rating.get_ratings_by_media()

        for review in context['reviews']:
            review.full_stars = range(review.rating)
            review.empty_stars = range(5 - review.rating)
            review.media_name = review.media.title

        return context


def add_media_view(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/media/')
    else:
        form = MediaForm()

    return render(request, 'add_media.html', {'form': form})


def manage_old_movies():
    old_movies = Movie.objects.filter(release_date__lt="2000-01-01", rating__lt=3)
    old_movies.update(is_published=False)
    old_movies.delete()
