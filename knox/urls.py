from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt
from knox import views

urlpatterns = [
    url(r'api/register/', csrf_exempt(views.RegisterView.as_view()), name='register-api'),
    url(r'api/token-check/', csrf_exempt(views.TokenCheckAPI.as_view()), name='token-check'),
    url(r'api/login/', csrf_exempt(views.LoginView.as_view()), name='knox_login'),
    url(r'api/logout/', csrf_exempt(views.LogoutView.as_view()), name='knox_logout'),
    url(r'api/logoutall/', csrf_exempt(views.LogoutAllView.as_view()), name='knox_logoutall'),
]
