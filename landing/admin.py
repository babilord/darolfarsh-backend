from django.contrib import admin
from .models import ContentCategory, Content


admin.site.register(Content)
admin.site.register(ContentCategory)
