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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from user_profile.models import Profile
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def health(request):
    return JsonResponse({"status": "ok", "module": "accounts"})


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    email = (data.get("email") or "").strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"detail": "Invalid email format"}, status=400)
    password = data.get("password") or ""
    re_password = data.get("re_password") or ""

    if not email or not password or not re_password:
        return JsonResponse({"detail": "email, password, re_password are required"}, status=400)

    if password != re_password:
        return JsonResponse({"detail": "Passwords do not match"}, status=400)

    if User.objects.filter(username=email).exists():
        return JsonResponse({"detail": "User already exists"}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password)
    Profile.objects.get_or_create(user=user)

    return JsonResponse({"detail": "User created", "id": user.id, "email": user.email}, status=201)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return JsonResponse(
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
        },
        status=200,
    )


def dbtz(request):
    connection.ensure_connection()
    tz = connection.connection.get_parameter_status("TimeZone")
    return JsonResponse({"db_timezone": tz})


def _pick(data, *keys, default=None):
    for k in keys:
        if k in data and data.get(k) is not None:
            return data.get(k)
    return default


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user

    first_name = _pick(request.data, "first_name", "firstName")
    last_name = _pick(request.data, "last_name", "lastName")
    phone = _pick(request.data, "phone", "phoneNumber", "phone_number")

    changed = False

    if first_name is not None:
        user.first_name = str(first_name).strip()
        changed = True

    if last_name is not None:
        user.last_name = str(last_name).strip()
        changed = True

    if changed:
        user.save()

    profile, _ = Profile.objects.get_or_create(user=user)

    if phone is not None:
        phone_value = str(phone).strip()

        if hasattr(profile, "phone"):
            profile.phone = phone_value
            profile.save()
            changed = True
        elif hasattr(profile, "phone_number"):
            profile.phone_number = phone_value
            profile.save()
            changed = True
        else:
            return Response(
                {"detail": "Profile model has no phone field (phone / phone_number). Add it and migrate."},
                status=400,
            )

    if not changed:
        return Response({"detail": "Nothing to update"}, status=400)

    return Response(
        {
            "detail": "Profile updated",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "profile": {
                "phone": getattr(profile, "phone", getattr(profile, "phone_number", None)),
            },
        },
        status=200,
    )

@api_view(["POST"])
def forgot_password(request):
    email = (request.data.get("email") or "").strip().lower()
    if not email:
        return Response({"detail": "email is required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        # امنیتی: لو نده ایمیل وجود دارد یا نه
        return Response({"detail": "If that email exists, a reset link was sent."}, status=200)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    frontend = getattr(settings, "FRONTEND_BASE_URL", "http://localhost:3000")
    reset_link = f"{frontend}/reset-password?uid={uid}&token={token}"

    subject = "Reset your password"
    message = f"Click the link to reset your password:\n\n{reset_link}"

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({"detail": f"Email sending failed: {str(e)}"}, status=500)

    return Response({"detail": "If that email exists, a reset link was sent."}, status=200)



@api_view(["POST"])
def reset_password(request):
    uidb64 = request.data.get("uid")
    token = request.data.get("token")
    password = request.data.get("password")
    re_password = request.data.get("re_password")

    if not uidb64 or not token or not password or not re_password:
        return Response({"detail": "uid, token, password, re_password are required"}, status=400)

    if password != re_password:
        return Response({"detail": "Passwords do not match"}, status=400)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"detail": "Invalid uid"}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"detail": "Invalid or expired token"}, status=400)

    user.set_password(password)  # اینجا hash میشه
    user.save()

    return Response({"detail": "Password reset successful"}, status=200)
