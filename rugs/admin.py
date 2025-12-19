from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter
from .models import Rug, KnotType, RugType, YarnType, RugCorner, RugBackground, RugToranj, RugBorder, RugTile, UserRug, \
    RugLog, RugPart, RugPartType, RugReplacement, CustomRugSize, CustomRugRequest


@admin.register(Rug)
class RugAdmin(ModelAdmin):
    list_filter = ('rug_type',)
    readonly_fields = ('created',)
    list_display = ('name', 'rug_type')


admin.site.register(YarnType)
admin.site.register(RugType)
admin.site.register(KnotType)
# admin.site.register(RugBorder)
# admin.site.register(RugCorner)
# admin.site.register(RugBackground)
# admin.site.register(RugToranj)
# admin.site.register(RugTile)
# admin.site.register(UserRug)
admin.site.register(RugLog)
admin.site.register(RugPart)
admin.site.register(RugPartType)
admin.site.register(RugReplacement)
admin.site.register(CustomRugSize)
admin.site.register(CustomRugRequest)
