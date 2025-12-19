from rest_framework import serializers
from room.models import DecorationType, Decoration, Wall, Floor, Ceiling


class DecorationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecorationType
        fields = ['id', 'name']


class DecorationSerializer(serializers.ModelSerializer):
    decoration_type = DecorationTypeSerializer()

    class Meta:
        model = Decoration
        fields = ['id', 'name', 'decoration_type', 'image', 'position_left', 'position_right', 'position_top',
                  'position_bottom']


class WallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wall
        fields = ['id', 'name', 'front_image', 'left_image', 'right_image']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'name', 'image']


class CeilingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceiling
        fields = ['id', 'name', 'image', 'color_code']

