from rest_framework import mixins, status, viewsets, filters, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Auth, User
from reviews.models import Genre, Category, Title
from .permissions import IsAdminOrReadOnly
from .serializers import UsersSerializer, SingUpSerializer, RetrieveTokenSerializer, TitleSerializer, CategorySerializer, GenreSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SingUpSerializer

class RetrieveTokenView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = RetrieveTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.data["user"])
            user.is_active = True
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
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'category',
        'genre',
        'name',
        'year',
    )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
