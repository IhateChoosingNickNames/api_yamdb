from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, SignUpViewSet, RetrieveTokenView, CategoryViewSet, GenreViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register(r'auth/signup', SignUpViewSet, basename="signup")
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(
    'titles',
    TitleViewSet
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', RetrieveTokenView.as_view())

]

