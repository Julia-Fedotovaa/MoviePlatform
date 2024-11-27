from rest_framework import serializers

from .models import Genre, Country, Movie, TVShow, Rating
from .validators import validate_title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_title])

    class Meta:
        model = Movie
        fields = '__all__'


class TVShowSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    country = CountrySerializer()

    class Meta:
        model = TVShow
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
