from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import Auth, User
from reviews.models import Genre, Category, Title, Review, Comment, Rating


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


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
    user = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_confirmation_code(self, value):
        auth = get_object_or_404(Auth, user_id=self.initial_data["user"])
        if auth.confirmation_code != value:
            raise serializers.ValidationError("Некорретный код подтверждения.")
        return value


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
            'rating')


# Заглушки
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"