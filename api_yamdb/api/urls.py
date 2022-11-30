from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, SignUpViewSet, RetrieveTokenView

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register(r'auth/signup', SignUpViewSet, basename="signup")



urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', RetrieveTokenView.as_view())

]