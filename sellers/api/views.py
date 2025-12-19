from rest_framework import generics
from .serializers import SellerSerializer
from sellers.models import Seller


class SellersListAPI(generics.ListAPIView):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
