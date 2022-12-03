from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import Auth, User
from reviews.models import Genre, Category, Title, Review, Comment, Rating


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")

    def update(self, instance, validated_data):

        if "role" in validated_data:
            del validated_data["role"]
        return super().update(instance, validated_data)


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    @staticmethod
    def generate_code():
        import random
        tmp = [str(i) for i in range(10)]
        random.shuffle(tmp)
        return ''.join(tmp)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Недопустимое имя пользователя")
        return value

    def create(self, validated_data):
        confirmation_code = self.generate_code()
        email = mail.EmailMessage(subject='YaMDb', body=f"{confirmation_code}", from_email="site-owner@email.world", to=[validated_data['email']])
        email.send()
        print(mail.outbox[0].body)
        user = User.objects.create_user(**validated_data)
        Auth.objects.create(user=user, confirmation_code=confirmation_code)
        return user


class RetrieveTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")

    def validate(self, attrs):
        auth = get_object_or_404(Auth, user__username=self.initial_data.get("username"))
        if auth.confirmation_code != attrs["confirmation_code"]:
            raise serializers.ValidationError("Некорретный код подтверждения.")
        return attrs


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
            'id',
            'name',
            'year',
            'genre',
            'description',
            'category',
        )

    def to_representation(self, instance):
        representation = super(TitleSerializer, self).to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = []
        for entry in instance.genre.all():
            genre = GenreSerializer(entry).data
            representation['genre'].append(genre)
        return representation




# Заглушки
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
