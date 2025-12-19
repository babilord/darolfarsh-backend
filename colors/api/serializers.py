from rest_framework.serializers import ModelSerializer
from colors.models import Color


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'color_code', 'hex_code', 'decimal_code']

