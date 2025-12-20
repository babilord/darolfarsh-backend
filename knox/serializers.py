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
        # اگر پروفایل یا language وجود نداشت کرش نکن
        profile = getattr(obj, "profile", None)
        lang = getattr(profile, "language", None)

        # اگر language یک آبجکت باشه (ForeignKey) و code داشته باشه
        if hasattr(lang, "code"):
            return lang.code

        # اگر language مثلا یک string باشه
        return lang  # یا می‌تونی return "en" بذاری
