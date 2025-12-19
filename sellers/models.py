from django.db import models
from cities.models import City
from manufacturers.models import Manufacturer
from rugs.models import Rug


class Seller(models.Model):
    name = models.CharField(null=False, blank=False, max_length=260)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(null=True, blank=True, max_length=360)
    phone = models.CharField(null=True, blank=True, max_length=25)
    admin_name = models.CharField(null=True, blank=True, max_length=360)
    brands = models.ManyToManyField(Manufacturer, blank=True, related_name="brands")
    representations = models.ManyToManyField(Manufacturer, blank=True, related_name="representations")
    rugs = models.ManyToManyField(Rug, through="SellerRug")
    map_url = models.URLField(null=True, blank=True, max_length=1000)
    vr_file = models.FileField(null=True, blank=True, upload_to="vr_files")
    logo = models.ImageField(null=True, blank=True, upload_to="sellers")

    def __str__(self):
        return self.name


class SellerRug(models.Model):
    seller = models.ForeignKey(Seller, null=False, blank=False, on_delete=models.CASCADE)
    rug = models.ForeignKey(Rug, null=False, blank=False, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    price = models.IntegerField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)
    available_sizes = models.IntegerField(default=1)
    buy_url = models.URLField(null=True, blank=True)

    def __str__(self):
        available_string = "Available" if self.available else "Not Available"
        return self.seller.name + " - " + self.rug.name + ": " + available_string + " - " + str(self.price)
