from django.contrib import admin
from .models import DecorationType, Decoration, Wall, Floor, Ceiling


admin.site.register(DecorationType)
admin.site.register(Decoration)
admin.site.register(Wall)
admin.site.register(Floor)
admin.site.register(Ceiling)
