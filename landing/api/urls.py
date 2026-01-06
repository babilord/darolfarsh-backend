from django.urls import path
from .views import ContentListAPI
from .views import LoginAPI


app_name = "landing-api"
urlpatterns = [
    path('contents/', ContentListAPI.as_view(), name="contents"),
    path('user/login/', LoginAPI.as_view(), name="user-login"),

]
