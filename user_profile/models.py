from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(null=True, blank=True, max_length=25)

    def __str__(self):
        return str(self.user.username)
