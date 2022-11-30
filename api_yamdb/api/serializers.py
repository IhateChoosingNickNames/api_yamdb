from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер модели категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер модели жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'genre',
            'description',
            'category',
            'raiting')
