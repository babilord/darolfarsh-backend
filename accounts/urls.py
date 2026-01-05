from django.urls import path
from knox import views as knox_views
from django.views.decorators.csrf import csrf_exempt
from .views import KnoxLoginAPI
from .views import (
    health,
    register,
    me,
    dbtz,
    update_profile,
    forgot_password,
    reset_password,
)

app_name = "accounts-api"
urlpatterns = [
    path("health/", csrf_exempt(health)),
    path("register/", csrf_exempt(register)),

    # Knox login/logout
    #path("login/", KnoxLoginAPI.as_view(), name="knox_login"),
    path("login/", csrf_exempt(knox_views.LoginView.as_view()), name="knox_login"),
    path("logout/", csrf_exempt(knox_views.LogoutView.as_view()), name="knox_logout"),
    path("logoutall/", csrf_exempt(knox_views.LogoutAllView.as_view()), name="knox_logoutall"),

    # current user
    path("me/", me),

    # update profile
    path("profile/", update_profile),  # PATCH /accounts/api/profile/

    # debug timezone
    path("dbtz/", dbtz),

    # forgot/reset password
    path("forgot-password/", forgot_password),
    path("reset-password/", reset_password),
]
