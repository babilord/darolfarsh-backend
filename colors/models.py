from django.db import models


class Color(models.Model):
    name = models.CharField(null=False, blank=False, max_length=160)
    color_code = models.CharField(null=True, blank=True, max_length=160)
    hex_code = models.CharField(null=False, blank=False, max_length=160)
    decimal_code = models.CharField(null=True, blank=True, max_length=160)

    def __str__(self):
        return self.name
