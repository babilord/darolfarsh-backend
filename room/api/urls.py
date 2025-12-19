from django.urls import path
from .views import RoomPartsAPI

app_name = "room-api"
urlpatterns = [
    path('parts/', RoomPartsAPI.as_view(), name="room-parts"),
]
