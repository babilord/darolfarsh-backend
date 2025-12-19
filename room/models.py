from django.db import models


class DecorationType(models.Model):
    name = models.CharField(null=False, blank=False, max_length=200)

    def __str__(self):
        return self.name


class Decoration(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60)
    decoration_type = models.ForeignKey(DecorationType, null=False, blank=False, on_delete=models.PROTECT,
                                        related_name="decorations")
    image = models.ImageField(null=False, blank=False, upload_to='room/decorations')
    # Position
    position_left = models.CharField(null=True, blank=True, max_length=10)
    position_right = models.CharField(null=True, blank=True, max_length=10)
    position_top = models.CharField(null=True, blank=True, max_length=10)
    position_bottom = models.CharField(null=True, blank=True, max_length=10)

    def __str__(self):
        return self.name + " - " + self.decoration_type.name


class Wall(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60)
    # decoration_type = models.ForeignKey(DecorationType, null=False, blank=False, on_delete=models.PROTECT,
    #                                     related_name="walls")
    front_image = models.ImageField(null=False, blank=False, upload_to='room/walls')
    left_image = models.ImageField(null=False, blank=False, upload_to='room/walls')
    right_image = models.ImageField(null=False, blank=False, upload_to='room/walls')

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60)
    # decoration_type = models.ForeignKey(DecorationType, null=False, blank=False, on_delete=models.PROTECT,
    #                                     related_name="floors")
    image = models.ImageField(null=False, blank=False, upload_to='room/floors')

    def __str__(self):
        return self.name


class Ceiling(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60)
    image = models.ImageField(null=True, blank=True, upload_to='room/roofs')
    color_code = models.CharField(null=True, blank=True, max_length=60)

    def __str__(self):
        return self.name + " - " + str(self.color_code)
