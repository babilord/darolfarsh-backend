from rest_framework import generics, status
from rugs.api.serializers import CustomRugRequestSerializer
from .serializers import ContentCategorySerializer
from .serializers import ContentLoginSerializer

from landing.models import ContentCategory
from landing.models import LoginModel
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db import connection
from django.http import JsonResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from user_profile.models import Profile
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class ContentListAPI(generics.ListAPIView):
    serializer_class = ContentCategorySerializer
    queryset = ContentCategory.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(generics.GenericAPIView):
    serializer_class = ContentLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "email/username and password required"}, status=400)

        serializer = AuthTokenSerializer(data={
            "username": username,
            "password": password
        })
        serializer.is_valid(raise_exception=True)

        # Get authenticated user
        user = serializer.validated_data["user"]

        # Create Knox token
        expires = (None if request.data.get('rememberme', False) else True)
        token = AuthToken.objects.create(user=user, expires=expires)

        # Send login signal
        user_logged_in.send(sender=user.__class__, request=request, user=user)

        # Serialize user
        UserSerializer = knox_settings.USER_SERIALIZER
        context = {'request': request, 'format': self.format_kwarg, 'view': self}

        return Response({
            'user': UserSerializer(user, context=context).data,
            'token': token,
        })
