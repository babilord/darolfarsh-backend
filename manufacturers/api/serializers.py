from manufacturers.models import Manufacturer
from rest_framework import serializers


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name']
