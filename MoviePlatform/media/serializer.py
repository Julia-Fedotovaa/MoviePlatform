from django.contrib.contenttypes.models import ContentType
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
    genres = GenreSerializer(many=True)
    country = CountrySerializer()

    class Meta:
        model = Movie
        fields = '__all__'


class TVShowSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_title])
    genres = GenreSerializer(many=True)
    country = CountrySerializer()

    class Meta:
        model = TVShow
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField(read_only=True)
    media_choice = serializers.ChoiceField(
        choices=[],
        write_only=True,
        label="Выберите медиа"
    )
    rating = serializers.IntegerField(min_value=1, max_value=10, label="Оценка")

    class Meta:
        model = Rating
        fields = ['id', 'rating', 'media_choice', 'media', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        media_choices = [
            *[(f'movie-{movie.id}', f'Фильм: {movie.title}') for movie in Movie.objects.all()],
            *[(f'tvshow-{tvshow.id}', f'Сериал: {tvshow.title}') for tvshow in TVShow.objects.all()]
        ]
        self.fields['media_choice'].choices = media_choices

    def get_media(self, obj):
        try:
            if obj.media.get_media_type() == ContentType.objects.get_for_model(Movie):
                print(MovieSerializer(obj.media).data)

                return MovieSerializer(obj.media).data

            elif obj.media.get_media_type() == ContentType.objects.get_for_model(TVShow):
                print(TVShowSerializer(obj.media).data)

                return TVShowSerializer(obj.media).data

        except Exception as e:
            print(e)
            return None

    def validate_media_choice(self, value):
        try:
            media_type, media_id = value.split('-')
            media_id = int(media_id)
        except ValueError:
            raise serializers.ValidationError("Неверный формат выбора медиа.")

        if media_type == "movie":
            if not Movie.objects.filter(id=media_id).exists():
                raise serializers.ValidationError("Выбранный фильм не найден.")
        elif media_type == "tvshow":
            if not TVShow.objects.filter(id=media_id).exists():
                raise serializers.ValidationError("Выбранный сериал не найден.")
        else:
            raise serializers.ValidationError("Неизвестный тип медиа.")

        return value

    def create(self, validated_data):
        media_type, media_id = validated_data.pop('media_choice').split('-')
        media = None
        if media_type == "movie":
            media = Movie.objects.get(id=media_id)
        elif media_type == "tvshow":
            media = TVShow.objects.get(id=media_id)

        rating = Rating.objects.create(media=media, **validated_data)
        return rating
