from sellers.models import Seller
from rest_framework import serializers
from cities.api.serializers import CitySerializer


class SellerSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'name', 'city', 'address', 'phone', 'admin_name', 'map_url', 'vr_file', 'logo']

    def get_city(self, obj):
        return CitySerializer(obj).data
