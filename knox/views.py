from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from django.contrib.auth.models import User
from user_profile.models import Profile
from .utils import email_validator, password_validator
from rest_framework.exceptions import NotAcceptable
from user_profile.api.serializers import UserPrivateSerializer


class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        expires = (None if request.POST.get('rememberme', False) else True)
        token = AuthToken.objects.create(request.user, expires=expires)
        user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        UserSerializer = knox_settings.USER_SERIALIZER
        context = {'request': self.request, 'format': self.format_kwarg, 'view': self}
        return Response({
            'user': UserSerializer(request.user, context=context).data,
            'token': token,
        })


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):

    def post(self, request):
        context = {}
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        email_validation = email_validator(email)
        password_validation = password_validator(password)
        if not email_validation["valid"]:
            raise NotAcceptable(code=400, detail=email_validation["error"])
        if not password_validation["valid"]:
            raise NotAcceptable(code=400, detail=password_validation["error"])

        user = User.objects.create(username=email, email=email)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, phone_number=phone)

        token = AuthToken.objects.create(user, expires=True)

        context["status"] = "ok"
        context["token"] = token
        context["email"] = email

        return Response(context, status=200)


class CredentialsValidation(APIView):

    def post(self, request):
        context = {}
        email = request.GET.get('email', None)
        if email and email == 'True' and request.POST.get('email', False):
            context['email'] = (
                False if User.objects.filter(email__iexact=request.POST.get('email')).exists() else True)

        return Response(context)


class TokenCheckAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        user_data = UserPrivateSerializer(user).data

        context = {
            'status': 'ok',
            'user': user_data
        }

        return Response(context)
