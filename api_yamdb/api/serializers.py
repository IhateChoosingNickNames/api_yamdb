from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'description', 'category')
