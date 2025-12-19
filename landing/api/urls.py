from django.urls import path
from .views import ContentListAPI

app_name = "landing-api"
urlpatterns = [
    path('contents/', ContentListAPI.as_view(), name="contents"),
]
