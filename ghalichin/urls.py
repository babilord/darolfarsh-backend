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
from .utils import move
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('knox.urls')),
    path('blog/api/', include('blog.api.urls', namespace="blog-api")),
    path('rug/api/', include('rugs.api.urls', namespace="rug-api")),
    path('room/api/', include('room.api.urls', namespace="room-api")),
    path('sellers/api/', include('sellers.api.urls', namespace="sellers-api")),
    path('landing/api/', include('landing.api.urls', namespace="landing-api")),
    # path('utils/move/', move)
    path('accounts/api/', include('accounts.urls')),
]
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^m/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]