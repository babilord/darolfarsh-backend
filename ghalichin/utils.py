from django.http import HttpResponse
from rugs.models import RugType, Rug, RugPart, RugToranj, RugTile, RugBackground, RugBorder, RugCorner, RugPartType


def move(request):
    corners = RugCorner.objects.all()
    borders = RugBorder.objects.all()
    toranjs = RugToranj.objects.all()
    backgrounds = RugBackground.objects.all()
    tiles = RugTile.objects.all()

    corner_type, created = RugPartType.objects.get_or_create(name="corner")
    border_type, created = RugPartType.objects.get_or_create(name="border")
    # background_type, created = RugPartType.objects.get_or_create(name="background")
    # afshan_background_type, created = RugPartType.objects.get_or_create(name="afshan_background")
    toranj_type, created = RugPartType.objects.get_or_create(name="toranj")
    tile_type, created = RugPartType.objects.get_or_create(name="tile")

    # for corner in corners:
    #     part = RugPart()
    #     part.name = corner.name + " corner"
    #     part.part_type = corner_type
    #     part.image = corner.image
    #     part.save()

    # for border in borders:
    #     part = RugPart()
    #     part.name = border.name + " border"
    #     part.part_type = border_type
    #     part.image = border.image
    #     part.save()

    # for toranj in toranjs:
    #     part = RugPart()
    #     part.name = toranj.name + " toranj"
    #     part.part_type = toranj_type
    #     part.image = toranj.image
    #     part.save()

    # for tile in tiles:
    #     part = RugPart()
    #     part.name = tile.name + " tile"
    #     part.part_type = tile_type
    #     part.image = tile.image
    #     part.save()

    # for background in backgrounds:
    #     part = RugPart()
    #     part.name = background.name + " background"
    #     background_type, created = RugPartType.objects.get_or_create(name=background.rug_types.first().name + "_background")
    #     part.part_type = background_type
    #     part.image = background.image
    #     part.save()
    #     for rug in background.rug_types.all():
    #         part.rug_types.add(rug)
    
    rugs = Rug.objects.all()
    for rug in rugs:
        if rug.corner:
            rug_part, created = RugPart.objects.get_or_create(
                name=rug.corner.name + " corner", part_type=corner_type, image=rug.corner.image
            )
            rug.corner_n = rug_part
        if rug.tile:
            rug_part, created = RugPart.objects.get_or_create(
                name=rug.tile.name + " tile", part_type=tile_type, image=rug.tile.image
            )
            rug.tile_n = rug_part
        if rug.border:
            rug_part, created = RugPart.objects.get_or_create(
                name=rug.border.name + " border", part_type=border_type, image=rug.border.image
            )
            rug.border_n = rug_part
        if rug.toranj:
            rug_part, created = RugPart.objects.get_or_create(
                name=rug.toranj.name + " toranj", part_type=toranj_type, image=rug.toranj.image
            )
            rug.toranj_n = rug_part
        if rug.background:
            background_type, created = RugPartType.objects.get_or_create(name=rug.background.rug_types.first().name + "_background")
            rug_part, created = RugPart.objects.get_or_create(
                name=rug.background.name + " " + background_type.name, part_type=background_type, image=rug.background.image
            )
            rug.background_n = rug_part
        rug.save()


    return HttpResponse("ok")
