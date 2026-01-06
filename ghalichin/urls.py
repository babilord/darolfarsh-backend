"""ghalichin URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url="https://api.daralfarsha.com", 
)

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})





urlpatterns = [
    # Swagger UI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc UI
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Raw JSON/YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('auth/', include('knox.urls')),
    path('blog/api/', include('blog.api.urls', namespace="blog-api")),
    path('rug/api/', include('rugs.api.urls', namespace="rug-api")),
    path('room/api/', include('room.api.urls', namespace="room-api")),
    path('sellers/api/', include('sellers.api.urls', namespace="sellers-api")),
    path('landing/api/', include('landing.api.urls', namespace="landing-api")),
    path('accounts/api/', include('accounts.api.urls', namespace="accounts-api")),
    #path("csrf/", get_csrf),
    # path('utils/move/', move)
    

]
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^m/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]