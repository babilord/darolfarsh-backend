from django.urls import path
from .views import SellersListAPI

app_name = "sellers-api"
urlpatterns = [
    path('list/', SellersListAPI.as_view(), name="sellers-list"),
]
