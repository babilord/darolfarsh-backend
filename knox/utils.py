from django.contrib.auth.models import User


def email_validator(email):
    if not 40 > len(email) > 10:
        return {"valid": False, "error": "Email should be longer than 10 and shorter than 40"}
    if User.objects.filter(email=email).count() > 0:
        return {"valid": False, "error": "Email is already taken"}
    return {"valid": True}


def password_validator(password):
    if not 37 > len(password) >= 8:
        return {"valid": False, "error": "Password should be longer than 7 and shorter than 37"}
    return {"valid": True}
