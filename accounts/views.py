import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.db import connection

# اگر پروفایل باید ساخته شود
from user_profile.models import Profile

# برای me/
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication


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
    password = data.get("password") or ""
    re_password = data.get("re_password") or ""

    if not email or not password or not re_password:
        return JsonResponse({"detail": "email, password, re_password are required"}, status=400)

    if password != re_password:
        return JsonResponse({"detail": "Passwords do not match"}, status=400)

    if User.objects.filter(username=email).exists():
        return JsonResponse({"detail": "User already exists"}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password)

    # اگر سیستم شما به Profile وابسته است، بساز
    Profile.objects.get_or_create(user=user)

    return JsonResponse({"detail": "User created", "id": user.id, "email": user.email}, status=201)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return JsonResponse({
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "first_name": u.first_name,
        "last_name": u.last_name,
    }, status=200)


def dbtz(request):
    connection.ensure_connection()
    tz = connection.connection.get_parameter_status("TimeZone")
    return JsonResponse({"db_timezone": tz})
