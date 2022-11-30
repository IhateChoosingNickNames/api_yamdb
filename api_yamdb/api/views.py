from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from users.models import Auth, User
from .serializers import UsersSerializer, SingUpSerializer, RetrieveTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class SignUpViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SingUpSerializer

class RetrieveTokenView(APIView):
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
