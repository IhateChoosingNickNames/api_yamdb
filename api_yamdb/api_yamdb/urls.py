from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api_yamdb import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
