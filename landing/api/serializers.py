from landing.models import Content, ContentCategory, LoginModel
from rest_framework import serializers


class ContentSerializer(serializers.ModelSerializer):
    short_text = serializers.SerializerMethodField()
    long_text = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['short_text', 'media_url', 'long_text']

    def get_short_text(self, obj):
        return {
            "fa": obj.short_text_fa,
            "en": obj.short_text_en,
            "ar": obj.short_text_ar,
            "du": obj.short_text_du,
        }

    def get_long_text(self, obj):
        return {
            "fa": obj.long_text_fa,
            "en": obj.long_text_en,
            "ar": obj.long_text_ar,
            "du": obj.long_text_du,
        }


class ContentCategorySerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = ContentCategory
        fields = ['category', 'contents']

    def get_contents(self, obj):
        return ContentSerializer(obj.contents.all(), many=True).data
    

class ContentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginModel
        fields = ['username', 'password']

    def get_contents(self, obj):
        return ContentSerializer(obj.contents.all(), many=True).data
