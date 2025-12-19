from django.conf.urls import include, url

from knox import views

urlpatterns = [
    url(r'api/register/', views.RegisterView.as_view(), name='register-api'),
    url(r'api/token-check/', views.TokenCheckAPI.as_view(), name='token-check'),
    url(r'api/login/', views.LoginView.as_view(), name='knox_login'),
    url(r'api/logout/', views.LogoutView.as_view(), name='knox_logout'),
    url(r'api/logoutall/', views.LogoutAllView.as_view(), name='knox_logoutall'),
]
