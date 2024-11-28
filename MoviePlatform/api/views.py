from django.db.models import Q, Avg
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from media.models import Genre, Country, Movie, TVShow, Rating
from media.serializer import GenreSerializer, CountrySerializer, MovieSerializer, TVShowSerializer, RatingSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    sorting_fields = ['name']
    filter_backends = [SearchFilter]
    search_fields = ['name']


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    sorting_fields = ['name']
    filter_backends = [SearchFilter]
    search_fields = ['name']


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['country', 'release_date']
    sorting_fields = ['title', 'release_date', 'rating']

    @action(methods=['GET'], detail=False)
    def high_rated(self, request):
        high_rated_movies = Movie.objects.annotate(
            average_rating=Avg('abstractmedia_ptr__rating__rating')
        ).filter(average_rating__gt=4.0)

        serializer = self.get_serializer(high_rated_movies, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def add_rating(self, request, pk=None):
        movie = self.get_object()
        rating_value = request.data.get('rating')

        if rating_value:
            rating = Rating.objects.create(movie=movie, rating=rating_value)
            serializer = RatingSerializer(rating)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Rating value is required'}, status=status.HTTP_400_BAD_REQUEST)


class TVShowViewSet(viewsets.ModelViewSet):
    queryset = TVShow.objects.all()
    serializer_class = TVShowSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['country', 'release_date']
    sorting_fields = ['title', 'release_date', 'rating']

    @action(methods=['GET'], detail=False)
    def high_rated(self, request):
        high_rated_tvshows = TVShow.objects.annotate(
            average_rating=Avg('abstractmedia_ptr__rating__rating')
        ).filter(average_rating__gt=4.0)

        serializer = self.get_serializer(high_rated_tvshows, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def add_rating(self, request, pk=None):
        tvshow = self.get_object()
        rating_value = request.data.get('rating')

        if rating_value:
            rating = Rating.objects.create(media=tvshow, rating=rating_value)
            serializer = RatingSerializer(rating)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Rating value is required'}, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    sorting_fields = ['rating']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['rating', 'media', 'user']
    search_fields = ['media__title']


class ComplexQueryViewFirst(viewsets.ViewSet):
    def list(self, request):
        queryset = Movie.objects.filter(
            Q(title__icontains="a") |
            (~Q(country__name="USA") & Q(length__lt="02:00:00"))
        )

        serializer = MovieSerializer(queryset, many=True)

        return Response(serializer.data)


class ComplexQueryViewSecond(viewsets.ViewSet):
    def list(self, request):
        queryset = Rating.objects.filter(
            ~Q(rating__range=(1, 3)) & Q(media__title__icontains="a") | Q(media__country__name="Japan"))

        serializer = RatingSerializer(queryset, many=True)

        return Response(serializer.data)
