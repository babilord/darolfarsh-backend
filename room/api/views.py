from rest_framework.views import APIView
from rest_framework.response import Response
from room.models import Decoration, Wall, Floor, Ceiling
from .serializers import WallSerializer, DecorationSerializer, FloorSerializer, CeilingSerializer


class RoomPartsAPI(APIView):
    def get(self, request):
        data = {
            "decorations": {}
        }

        # Decorations
        decorations = Decoration.objects.all().select_related("decoration_type")
        for decoration in decorations:
            values = data["decorations"].get(decoration.decoration_type.name, [])
            values.append(DecorationSerializer(decoration, context={"request": request}).data)
            data["decorations"][decoration.decoration_type.name] = values

        walls = Wall.objects.all()
        floors = Floor.objects.all()
        roofs = Ceiling.objects.all()
        data["walls"] = WallSerializer(walls, many=True, context={"request": request}).data
        data["floors"] = FloorSerializer(floors, many=True, context={"request": request}).data
        data["ceilings"] = CeilingSerializer(roofs, many=True, context={"request": request}).data
        return Response(data)
