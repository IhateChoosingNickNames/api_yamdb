from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import relations, serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import Auth, User
from .utils import send_message


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор модели юзеров."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def update(self, instance, validated_data):
        """Запрет на изменение роли."""
        if "role" in validated_data:
            del validated_data["role"]
        return super().update(instance, validated_data)


class SingUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        """Дополнительная валидация юзернейма на уровне сериализатора."""
        if value == "me":
            raise serializers.ValidationError("Недопустимое имя пользователя.")
        return value

    def create(self, validated_data):
        """При создании пользователя админом - пользователь сразу активен.
        При самостоятельной регистрации - становится активным только после
        подтверждения.
        """
        confirmation_code = get_random_string()

        if not self.context["request"].user.is_staff:
            validated_data["is_active"] = False

        user = User.objects.create_user(**validated_data)
        Auth.objects.create(user=user, confirmation_code=confirmation_code)
        send_message(validated_data, confirmation_code)
        return user


class RetrieveTokenSerializer(serializers.Serializer):
    """Проверка кода подтверждения и выдача токена."""

    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ("username", "confirmation_code")

    def validate(self, attrs):
        auth = get_object_or_404(
            Auth, user__username=self.initial_data.get("username")
        )
        if auth.confirmation_code != attrs["confirmation_code"]:
            raise serializers.ValidationError("Некорретный код подтверждения.")
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категорий."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанров."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class CustomSlugRelatedField(relations.SlugRelatedField):
    """Переопределения ответа."""

    def to_representation(self, obj):
        return {
            obj._meta.fields[1].name: obj.name,
            obj._meta.fields[2].name: obj.slug,
        }


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер модели произведений."""

    category = CustomSlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), required=False
    )

    genre = CustomSlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        required=False,
        many=True,
    )
    rating = serializers.IntegerField(source="average", read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "genre",
            "description",
            "category",
            "rating",
        )
        read_only_fields = ("rating",)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "score", "author", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
