from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField


User = get_user_model()

username_field = User.USERNAME_FIELD if hasattr(User, 'USERNAME_FIELD') else 'username'


class UserSerializer(serializers.ModelSerializer):
    language = SerializerMethodField()

    class Meta:
        model = User
        fields = (username_field, 'first_name', 'last_name', 'language')

    def get_language(self, obj):
        if obj.profile.language:
            return obj.profile.language.code
        return 'en'
