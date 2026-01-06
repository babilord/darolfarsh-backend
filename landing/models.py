from django.db import models


class ContentCategory(models.Model):
    category = models.CharField(null=False, blank=False, max_length=50)

    class Meta:
        verbose_name = 'Content category'
        verbose_name_plural = 'Content categories'

    def __str__(self):
        return self.category


class Content(models.Model):
    short_text_fa = models.TextField(null=False, blank=False, max_length=2000)
    short_text_en = models.TextField(null=False, blank=False, max_length=2000)
    short_text_ar = models.TextField(null=False, blank=False, max_length=2000)
    short_text_du = models.TextField(null=False, blank=False, max_length=2000)
    media_url = models.URLField(null=True, blank=True, max_length=1000)
    long_text_fa = models.TextField(null=True, blank=True, max_length=8000)
    long_text_en = models.TextField(null=True, blank=True, max_length=8000)
    long_text_ar = models.TextField(null=True, blank=True, max_length=8000)
    long_text_du = models.TextField(null=True, blank=True, max_length=8000)
    category = models.ForeignKey(ContentCategory, null=False, blank=False, on_delete=models.CASCADE,
                                 related_name="contents")

    def __str__(self):
        return f'{self.category} - {self.short_text_fa[:20]} ...'
    

    
class LoginModel(models.Model):
    username = models.CharField(null=False, blank=False, max_length=250)
    password = models.CharField(null=False, blank=False, max_length=128)

    def __str__(self):
        return self.username
