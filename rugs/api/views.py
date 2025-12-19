from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from knox.auth import TokenAuthentication
from django.db.models import Count, Q
from rugs.models import Rug, RugToranj, RugTile, RugBackground, RugBorder, RugType, RugCorner, UserRug, RugPartType, \
    RugPart, YarnType, CustomRugSize
from .serializers import RugFinderSerializer, RugBackgroundSerializer, RugBorderSerializer, RugCornerSerializer, \
    RugTileSerializer, RugToranjSerializer, UserRugSerializer, RugTypeSerializer, RugSellersSerializer, \
    RugLogCreateSerializer, RugPartSerializer, RugYarnSerializer, RugReplacementSerializer, CustomRugRequestSerializer, \
    CustomRugSizeSerializer
from .pagination import RugPartLimitOffsetPagination
from sellers.models import SellerRug
from manufacturers.api.serializers import ManufacturerSerializer
from manufacturers.models import Manufacturer
from colors.models import Color
from colors.api.serializers import ColorSerializer
from cities.models import City
from cities.api.serializers import CitySerializer


class RugListAPI(generics.ListAPIView):
    serializer_class = RugFinderSerializer
    pagination_class = RugPartLimitOffsetPagination

    def get_queryset(self):
        rug_type = self.request.GET.getlist("rug_type")
        densities = self.request.GET.getlist("densities")
        shanehs = self.request.GET.getlist("shanehs")
        brands = self.request.GET.getlist("brands")
        yarns = self.request.GET.getlist("yarns")
        colors = self.request.GET.getlist("colors")
        sizes = self.request.GET.getlist("sizes")

        rugs = Rug.objects.all()

        if rug_type:
            rugs = rugs.filter(rug_type__name__in=rug_type)
        if len(densities) > 0:
            rugs = rugs.filter(Q(corner__density__in=densities) | Q(border__density__in=densities) | Q(
                toranj__density__in=densities) | Q(background__density__in=densities) | Q(
                tile__density__in=densities) | Q(pattern__density__in=densities))
        if len(shanehs) > 0:
            rugs = rugs.filter(Q(corner__shaneh__in=shanehs) | Q(border__shaneh__in=shanehs) | Q(
                toranj__shaneh__in=shanehs) | Q(background__shaneh__in=shanehs) | Q(
                tile__shaneh__in=shanehs) | Q(pattern__shaneh__in=shanehs))
        if len(brands) > 0:
            print(brands)
            rugs = rugs.filter(Q(corner__brand__in=brands) | Q(border__brand__in=brands) | Q(
                toranj__brand__in=brands) | Q(background__brand__in=brands) | Q(
                tile__brand__in=brands) | Q(pattern__brand__in=brands))
        if len(yarns) > 0:
            rugs = rugs.filter(Q(corner__yarn__in=yarns) | Q(border__yarn__in=yarns) | Q(
                toranj__yarn__in=yarns) | Q(background__yarn__in=yarns) | Q(
                tile__yarn__in=yarns) | Q(pattern__yarn__in=yarns))
        if len(colors) > 0:
            rugs = rugs.filter(Q(corner__colors__in=colors) | Q(border__colors__in=colors) | Q(
                toranj__colors__in=colors) | Q(background__colors__in=colors) | Q(
                tile__colors__in=colors) | Q(pattern__colors__in=colors) | Q(colors__in=colors))
        if len(sizes) > 0:
            q = None

            for size in sizes:
                if not q:
                    q = Q(rug_sizes__icontains=size)
                else:
                    q = q | Q(rug_sizes__icontains=size)
            rugs = rugs.filter(q)

        return rugs.distinct().order_by("id")


class RugFinderAPI(generics.ListAPIView):
    serializer_class = RugFinderSerializer
    queryset = Rug.objects.all()

    def get_queryset(self):
        toranj = self.request.GET.get("toranj", 0)
        corner = self.request.GET.get("corner", 0)
        background = self.request.GET.get("background", 0)
        border = self.request.GET.get("border", 0)
        tile = self.request.GET.get("tile", 0)
        pattern = self.request.GET.get("pattern", 0)
        rug_type = self.request.GET.get("rug_type")

        if not rug_type:
            raise NotAcceptable(detail="no rug type provided", code=400)

        return Rug.objects.filter(rug_type__pk=rug_type).annotate(
            similarity=(
                    Count("toranj", filter=Q(toranj__pk=toranj)) +
                    Count("corner", filter=Q(corner__pk=corner)) +
                    Count("background", filter=Q(background__pk=background)) +
                    Count("border", filter=Q(border__pk=border)) +
                    Count("tile", filter=Q(tile__pk=tile)) + Count("pattern", filter=Q(pattern__pk=pattern))
            )
        ).filter(similarity__gt=0).order_by("-similarity")[:4]


class NewRugPartsListAPI(generics.ListAPIView):
    serializer_class = RugPartSerializer
    pagination_class = RugPartLimitOffsetPagination

    def get_queryset(self):
        part_types = self.request.GET.getlist("part_type", "")

        rug_type = self.request.GET.get("rug_type")
        densities = self.request.GET.getlist("densities")
        shanehs = self.request.GET.getlist("shanehs")
        brands = self.request.GET.getlist("brands")
        yarns = self.request.GET.getlist("yarns")
        colors = self.request.GET.getlist("colors")

        parts = RugPart.objects.all()
        if len(part_types) > 0:
            parts = RugPart.objects.filter(part_type__name__in=part_types)

        if rug_type:
            parts = parts.filter(rug_types__name=rug_type)
        if len(densities) > 0:
            parts = parts.filter(density__in=densities)
        if len(shanehs) > 0:
            parts = parts.filter(shaneh__in=shanehs)
        if len(brands) > 0:
            parts = parts.filter(brand__in=brands)
        if len(yarns) > 0:
            parts = parts.filter(yarn__in=yarns)
        if len(colors) > 0:
            parts = parts.filter(colors__in=colors)

        return parts.order_by("id").distinct()


class RugPartListAPI(generics.ListAPIView):

    def get_serializer_class(self):
        part = self.request.GET.get("part")
        if not part:
            raise NotAcceptable(
                code=400, detail="no part name provided as GET parameter")
        if part.lower() == "corner":
            return RugCornerSerializer
        elif part.lower() == "border":
            return RugBorderSerializer
        elif part.lower() == "background":
            return RugBackgroundSerializer
        elif part.lower() == "tile":
            return RugTileSerializer
        elif part.lower() == "toranj":
            return RugToranjSerializer

    def get_queryset(self):
        part = self.request.GET.get("part")
        if not part:
            raise NotAcceptable(
                code=400, detail="no part name provided as GET parameter")
        if part.lower() == "corner":
            return RugCorner.objects.all().order_by("id")
        elif part.lower() == "border":
            return RugBorder.objects.all().order_by("id")
        elif part.lower() == "background":
            return RugBackground.objects.all().order_by("id")
        elif part.lower() == "tile":
            return RugTile.objects.all().order_by("id")
        elif part.lower() == "toranj":
            return RugToranj.objects.all().order_by("id")


class UserRugListAPI(generics.ListAPIView):
    serializer_class = UserRugSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    def get_queryset(self):
        return UserRug.objects.filter(user=self.request.user)


class UserRugDetailAPI(generics.RetrieveAPIView):
    serializer_class = UserRugSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    lookup_field = "pk"

    def get_queryset(self):
        return UserRug.objects.filter(user=self.request.user)


class RugTypListAPI(generics.ListAPIView):
    serializer_class = RugTypeSerializer
    queryset = RugType.objects.all()


class RugBrandsListAPI(generics.ListAPIView):
    serializer_class = ManufacturerSerializer

    def get_queryset(self):
        yarns = self.request.GET.getlist("yarn")
        shanehs = self.request.GET.getlist("shaneh")
        densities = self.request.GET.getlist("density")

        brands = Manufacturer.objects.all()
        if len(yarns) > 0:
            brands = brands.filter(rug_parts__yarn_id__in=yarns)

        if len(shanehs) > 0:
            brands = brands.filter(rug_parts__shaneh__in=shanehs)

        if len(densities) > 0:
            brands = brands.filter(rug_parts__density__in=densities)
        return brands.distinct()


class RugYarnsListAPI(generics.ListAPIView):
    serializer_class = RugYarnSerializer
    queryset = YarnType.objects.all()

    def get_queryset(self):
        brands = self.request.GET.getlist("brand")
        shanehs = self.request.GET.getlist("shaneh")
        densities = self.request.GET.getlist("density")

        yarns = YarnType.objects.all()
        if len(brands) > 0:
            yarns = yarns.filter(rug_parts__brand_id__in=brands)

        if len(shanehs) > 0:
            yarns = yarns.filter(rug_parts__shaneh__in=shanehs)

        if len(densities) > 0:
            yarns = yarns.filter(rug_parts__density__in=densities)
        return yarns.distinct()


class RugDensitiesListAPI(APIView):

    def get(self, request, format=None):
        brands = self.request.GET.getlist("brand")
        shanehs = self.request.GET.getlist("shaneh")
        yarns = self.request.GET.getlist("yarn")

        q = RugPart.objects.filter(density__isnull=False)

        if len(brands) > 0:
            q = q.filter(brand_id__in=brands)
        if len(yarns) > 0:
            q = q.filter(yarn_id__in=yarns)
        if len(shanehs) > 0:
            q = q.filter(shaneh__in=shanehs)
        return Response(list(q.distinct("density").values_list("density", flat=True)), 200)


class RugShanehsListAPI(APIView):

    def get(self, request, format=None):
        brands = self.request.GET.getlist("brand")
        densities = self.request.GET.getlist("density")
        yarns = self.request.GET.getlist("yarn")

        q = RugPart.objects.filter(shaneh__isnull=False)

        if len(brands) > 0:
            q = q.filter(brand_id__in=brands)
        if len(yarns) > 0:
            q = q.filter(yarn_id__in=yarns)
        if len(densities) > 0:
            q = q.filter(density__in=densities)
        return Response(list(q.distinct("shaneh").values_list("shaneh", flat=True)), 200)


class RugColorsListAPI(generics.ListAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class RugCitiesListAPI(generics.ListAPIView):
    serializer_class = CitySerializer
    pagination_class = RugPartLimitOffsetPagination

    def get_queryset(self):
        search = self.request.GET.get("q")
        if search:
            return City.objects.filter(name__icontains=search)
        return City.objects.all()


class RugSellersListAPI(generics.ListAPIView):
    serializer_class = RugSellersSerializer
    pagination_class = RugPartLimitOffsetPagination

    def get_queryset(self):
        rug_id = self.kwargs.get("pk")
        order = self.request.GET.get("order")
        cities = self.request.GET.getlist("cities")
        if not rug_id:
            raise NotAcceptable
        queryset = SellerRug.objects.filter(rug__pk=rug_id, available=True)
        if len(cities) > 0:
            queryset = queryset.filter(seller__city_id__in=cities)
        if order:
            if order == "on_sale":
                queryset = queryset.order_by("-on_sale")
            elif order == "cheapest":
                queryset = queryset.order_by("price")
            elif order == "most_expensive":
                queryset = queryset.order_by("-price")
            elif order == "oldest":
                queryset = queryset.order_by("-pk")
        else:
            queryset = queryset.order_by("pk")
        return queryset


class RugLogCreateAPI(generics.CreateAPIView):
    serializer_class = RugLogCreateSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        serializer.save(user=user, user_ip=ip)


class RugReplacementFormAPI(generics.CreateAPIView):
    serializer_class = RugReplacementSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req = self.perform_create(serializer)
        return Response({"status": "OK", "code": req.get_request_code()}, status=status.HTTP_201_CREATED)


class CustomRugSizeListAPI(generics.ListAPIView):
    serializer_class = CustomRugSizeSerializer
    queryset = CustomRugSize.objects.all()


class CustomRugRequestAPI(generics.CreateAPIView):
    serializer_class = CustomRugRequestSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req = self.perform_create(serializer)
        return Response({"status": "OK", "code": req.get_request_code()}, status=status.HTTP_201_CREATED)
