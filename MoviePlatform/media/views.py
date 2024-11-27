from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from media.models import Genre, Country, Movie, TVShow, Rating
from media.serializer import GenreSerializer, CountrySerializer, MovieSerializer, TVShowSerializer, RatingSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'release_date']



class TVShowViewSet(viewsets.ModelViewSet):
    queryset = TVShow.objects.all()
    serializer_class = TVShowSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class ComplexQueryView(APIView):
    def get(self, request):
        queryset = Movie.objects.filter(
            Q(title__icontains="a") |
            (~Q(country__name="USA") & Q(length__lt="02:00:00"))
        )

        serializer = MovieSerializer(queryset, many=True)

        return Response(serializer.data)
