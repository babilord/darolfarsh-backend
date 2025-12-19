from django.db import models


class City(models.Model):
    name = models.CharField(blank=False, null=False, max_length=120)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name
