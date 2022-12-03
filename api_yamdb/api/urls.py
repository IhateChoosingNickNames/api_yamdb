import rest_framework_simplejwt.authentication
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, SignUpViewSet, RetrieveTokenView, CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet, PatchUser

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register(r'auth/signup', SignUpViewSet, basename="signup")
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
# Заглушки
router_v1.register(r'titles/(?P<title_id>[1-9]\d*)/reviews', ReviewViewSet, basename="111")
router_v1.register(r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<review_id>[1-9]\d*)/comments', CommentViewSet, basename="review_comments")
router_v1.register(r'rating', ReviewViewSet)


urlpatterns = [
    path('v1/users/me/', PatchUser.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', RetrieveTokenView.as_view()),
]

