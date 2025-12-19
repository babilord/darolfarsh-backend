from django.db import models
from cities.models import City


class Manufacturer(models.Model):
    name = models.CharField(null=False, blank=False, max_length=200)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(null=True, blank=True, max_length=360)

    def __str__(self):
        return self.name + " - " + str(self.address)

