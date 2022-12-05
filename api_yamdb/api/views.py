from django.shortcuts import get_object_or_404
from rest_framework import (exceptions, filters, generics, mixins, response,
                            status, views, viewsets)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import Auth, User

from .filters import CustomSearchFilter
from .pagination import CustomPagination
from .permissions import (IsAdmin, IsAdminOrModOrReadOnly, IsAdminOrReadOnly,
                          IsAuthorOrAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RetrieveTokenSerializer,
                          ReviewSerializer, SingUpSerializer, TitleSerializer,
                          UsersSerializer)
from .utils import generate_code, send_message


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет юзеров."""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    pagination_class = CustomPagination
    lookup_field = "username"


class RetrievePatchUser(generics.RetrieveUpdateAPIView):
    """Получение и обновления данных пользователя."""

    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrAdmin)

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Регистрация нового пользователя."""

    serializer_class = SingUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Создание нового пользователя.
        Если пользователь сам регистрируется - то создается новый пользователь
        и на почту отправляется код подтверждения.
        Если админ создает, то пользователь уже есть в системе и ему просто
        отправится код подтверждения.
        """

        user = User.objects.filter(**request.data)

        if user:
            confirmation_code = generate_code()
            send_message(request.data, confirmation_code)
            Auth.objects.filter(user=user[0]).update(
                confirmation_code=confirmation_code
            )
            return response.Response(
                {"confirmed": "Сообщение отправлено"},
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class RetrieveTokenView(views.APIView):
    """Получение токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Получение токена.
        Если пользователь существует и хочет обновить свой токен, то он
        отправит username. Если пользователь неактивен, то он должен ввести
        код подтверждения.
        """
        serializer = RetrieveTokenSerializer(data=request.data)
        user = User.objects.filter(username=request.data.get("username"))

        if (
            user
            and user[0].is_active
            and request.user.username == request.data["username"]
        ):
            refresh = RefreshToken.for_user(user[0])
            return response.Response(
                {"access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED,
            )
        if serializer.is_valid():
            user = User.objects.get(username=serializer.data["username"])
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            Auth.objects.get(user=user).delete()
            return response.Response(
                {"access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED,
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet():
    """Вьюсет для произведений."""

    pass


class CategoryViewSet():
    """Вьюсет для категорий."""

    pass


class GenreViewSet():
    """Вьюсет для жанров."""

    pass

class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrModOrReadOnly)
    pagination_class = CustomPagination

    def __get_title(self):
        return get_object_or_404(Title, id=self.kwargs["title_id"])

    def get_queryset(self):
        return self.__get_title().review.all()

    def perform_create(self, serializer):
        if Review.objects.filter(
            author=self.request.user, title=self.__get_title()
        ).exists():
            raise exceptions.ValidationError("Вы уже оставили свой отзыв.")
        serializer.save(author=self.request.user, title=self.__get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrModOrReadOnly)
    pagination_class = CustomPagination

    def __get_review(self):
        return get_object_or_404(Review, id=self.kwargs["review_id"])

    def get_queryset(self):
        return self.__get_review().comment.all().select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.__get_review())
