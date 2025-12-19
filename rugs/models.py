import os

from django.db import models
from colors.models import Color
from manufacturers.models import Manufacturer
from django.contrib.auth.models import User


class RugType(models.Model):
    name = models.CharField(null=False, blank=False, max_length=200)

    def __str__(self):
        return self.name


class YarnType(models.Model):
    name = models.CharField(null=False, blank=False, max_length=200)

    def __str__(self):
        return self.name


class KnotType(models.Model):
    name = models.CharField(null=False, blank=False, max_length=200)

    def __str__(self):
        return self.name


class RugCorner(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    image = models.ImageField(null=False, blank=False, upload_to='corners')

    def __str__(self):
        return str(self.pk) + " - " + str(self.name)


class RugBorder(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    image = models.ImageField(null=False, blank=False, upload_to='borders')

    def __str__(self):
        return str(self.pk) + " - " + str(self.name)


class RugToranj(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    image = models.ImageField(null=False, blank=False, upload_to='toranjs')

    def __str__(self):
        return str(self.pk) + " - " + str(self.name)


class RugBackground(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    image = models.ImageField(null=False, blank=False, upload_to='backgrounds')
    rug_types = models.ManyToManyField(RugType, blank=True)

    def __str__(self):
        return str(self.pk) + " - " + str(self.name)


class RugTile(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    image = models.ImageField(null=False, blank=False, upload_to='tiles')

    def __str__(self):
        return str(self.pk) + " - " + str(self.name)


class RugPartType(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60, unique=True)

    def __str__(self):
        return self.name


class RugPart(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    part_type = models.ForeignKey(RugPartType, null=False, blank=False, on_delete=models.PROTECT)
    image = models.ImageField(null=False, blank=False, upload_to='parts')
    # rug_types = models.ManyToManyField(RugType, blank=True)
    density = models.IntegerField(null=True, blank=True)
    shaneh = models.IntegerField(null=True, blank=True)
    brand = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.SET_NULL, related_name="rug_parts")
    yarn = models.ForeignKey(YarnType, null=True, blank=True, on_delete=models.SET_NULL, related_name="rug_parts")
    # knot = models.ForeignKey(KnotType, null=True, blank=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, blank=True, null=True, on_delete=models.SET_NULL)
    colors = models.ManyToManyField(Color, blank=True, related_name="parts_colors")
    coloring_code = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return str(self.pk) + " - " + str(self.name)


class Rug(models.Model):
    name = models.CharField(null=False, blank=False, max_length=200)
    rug_type = models.ForeignKey(RugType, null=False, blank=False, on_delete=models.PROTECT)
    w_density = models.IntegerField(null=True, blank=True)
    l_density = models.IntegerField(null=True, blank=True)
    coloring_code = models.CharField(null=True, blank=True, max_length=200)
    colors = models.ManyToManyField(Color, blank=True)
    # corner = models.ForeignKey(RugCorner, null=True, blank=True, on_delete=models.PROTECT)
    # border = models.ForeignKey(RugBorder, null=True, blank=True, on_delete=models.PROTECT)
    # toranj = models.ForeignKey(RugToranj, null=True, blank=True, on_delete=models.PROTECT)
    # background = models.ForeignKey(RugBackground, null=True, blank=True, on_delete=models.PROTECT)
    # tile = models.ForeignKey(RugTile, null=True, blank=True, on_delete=models.PROTECT)
    corner = models.ForeignKey(RugPart, null=True, blank=True, on_delete=models.PROTECT, related_name="corner_rugs")
    border = models.ForeignKey(RugPart, null=True, blank=True, on_delete=models.PROTECT, related_name="border_rugs")
    toranj = models.ForeignKey(RugPart, null=True, blank=True, on_delete=models.PROTECT, related_name="toranj_rugs")
    background = models.ForeignKey(RugPart, null=True, blank=True, on_delete=models.PROTECT,
                                   related_name="background_rugs")
    tile = models.ForeignKey(RugPart, null=True, blank=True, on_delete=models.PROTECT, related_name="tile_rugs")
    pattern = models.ForeignKey(RugPart, null=True, blank=True, on_delete=models.PROTECT, related_name="pattern_rugs")
    yarn = models.ForeignKey(YarnType, null=True, blank=True, on_delete=models.SET_NULL)
    knot = models.ForeignKey(KnotType, null=True, blank=True, on_delete=models.SET_NULL)
    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    full_image = models.ImageField(null=True, blank=True, upload_to='rugs')
    rug_sizes = models.CharField(null=True, blank=True, max_length=30)

    def __str__(self):
        return self.name


class UserRug(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=260)
    rug_type = models.ForeignKey(RugType, null=False, blank=False, on_delete=models.PROTECT)
    corner = models.ForeignKey(RugCorner, null=True, blank=True, on_delete=models.PROTECT)
    border = models.ForeignKey(RugBorder, null=True, blank=True, on_delete=models.PROTECT)
    toranj = models.ForeignKey(RugToranj, null=True, blank=True, on_delete=models.PROTECT)
    background = models.ForeignKey(RugBackground, null=True, blank=True, on_delete=models.PROTECT)
    tile = models.ForeignKey(RugTile, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class RugLog(models.Model):
    rug_type = models.ForeignKey(RugType, null=False, blank=False, on_delete=models.PROTECT)
    corner = models.ForeignKey(RugCorner, null=True, blank=True, on_delete=models.PROTECT)
    border = models.ForeignKey(RugBorder, null=True, blank=True, on_delete=models.PROTECT)
    toranj = models.ForeignKey(RugToranj, null=True, blank=True, on_delete=models.PROTECT)
    background = models.ForeignKey(RugBackground, null=True, blank=True, on_delete=models.PROTECT)
    tile = models.ForeignKey(RugTile, null=True, blank=True, on_delete=models.PROTECT)
    parts = models.ManyToManyField(RugPart, blank=True)
    user_ip = models.CharField(null=True, blank=True, max_length=15)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rug_type.name + " - " + str(self.created) + " - " + self.user_ip


class RugReplacement(models.Model):
    name = models.CharField(null=False, blank=False, max_length=80)
    phone = models.CharField(null=False, blank=False, max_length=11)
    national_id = models.CharField(null=True, blank=True, max_length=20)
    address = models.CharField(null=True, blank=True, max_length=300)
    rug_url = models.URLField(null=True, blank=True, max_length=1000)
    file = models.FileField(null=True, blank=True, upload_to="rug_replacements")

    class Meta:
        verbose_name = '------ Rug replacement request'
        verbose_name_plural = '------ Rug replacement requests'

    def __str__(self):
        return f'{self.name} - {self.phone}'

    def get_request_code(self):
        return f'RR-{self.id}-{self.phone[-5:]}'

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(RugReplacement, self).delete(*args, **kwargs)


class CustomRugSize(models.Model):
    height = models.IntegerField(null=False, blank=False)
    width = models.IntegerField(null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=60)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.width}X{self.height}: {self.price}'


class CustomRugRequest(models.Model):
    name = models.CharField(null=False, blank=False, max_length=80)
    phone = models.CharField(null=False, blank=False, max_length=11)
    national_id = models.CharField(null=True, blank=True, max_length=20)
    address = models.CharField(null=True, blank=True, max_length=300)
    image = models.ImageField(null=False, blank=False, upload_to="custom_rugs")
    size = models.ForeignKey(CustomRugSize, null=False, blank=False, on_delete=models.PROTECT)

    class Meta:
        verbose_name = '------ Custom rug request'
        verbose_name_plural = '------ Custom rug requests'

    def __str__(self):
        return f'{self.name} - {self.phone} - {self.size}'

    def get_request_code(self):
        return f'CR-{self.id}-{self.phone[-5:]}'

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(CustomRugRequest, self).delete(*args, **kwargs)
