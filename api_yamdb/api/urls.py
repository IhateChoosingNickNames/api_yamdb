from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
app_name = 'api_yamdb'

router = routers.DefaultRouter()
router.register('v1/categories', CategoryViewSet, basename='category')
router.register('v1/genres', GenreViewSet, basename='genres')
router.register(
    'v1/titles',
    TitleViewSet,
    basename='titles'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include(router.urls)),
]
