from django.urls import path
from knox import views as knox_views
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
    path("health/", health),
    path("register/", register),

    # Knox login/logout
    path("login/", knox_views.LoginView.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),

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
