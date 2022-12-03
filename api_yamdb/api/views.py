from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets, filters, views, generics, pagination
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Auth, User
from reviews.models import Genre, Category, Title, Comment, Review, Rating
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdmin, Smth
from .serializers import RatingSerializer, UsersSerializer, SingUpSerializer, RetrieveTokenSerializer, TitleSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    pagination_class = CustomPagination
    lookup_field = "username"

class PatchUser(generics.RetrieveUpdateAPIView):

    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SingUpSerializer
    permission_classes = [AllowAny]

    # переделать
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class RetrieveTokenView(views.APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RetrieveTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.data["username"])
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            Auth.objects.get(user=user).delete()
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # этот метод отладочный, его нужно будет убрать
    def get(self, request):
        cats = Auth.objects.all()
        serializer = RetrieveTokenSerializer(cats, many=True)
        return Response(serializer.data)

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (Smth,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'category',
        'genre',
        'name',
        'year',
    )
    pagination_class = CustomPagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (Smth, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = CustomPagination
    lookup_field = "slug"

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (Smth,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = CustomPagination
    lookup_field = "slug"
# Заглушки
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    def __get_title(self):
        return get_object_or_404(Review, id=self.kwargs["title_id"])

    def get_queryset(self):
        return self.__get_title().review.all()

class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer

    def __get_review(self):
        return get_object_or_404(Review, id=self.kwargs["review_id"])

    def get_queryset(self):
        return self.__get_review().comments.all().select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.__get_review())

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
