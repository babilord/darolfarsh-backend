from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rugs.models import Rug, RugCorner, RugTile, RugToranj, RugBackground, RugBorder, RugType, UserRug, YarnType, \
    KnotType, RugLog, RugPartType, RugPart, RugReplacement, CustomRugRequest, CustomRugSize
from sellers.models import SellerRug
from sellers.api.serializers import SellerSerializer
from manufacturers.api.serializers import ManufacturerSerializer
from colors.api.serializers import ColorSerializer


class RugTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugType
        fields = ['id', 'name']


class RugYarnTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YarnType
        fields = ['id', 'name']


class RugKnotTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnotType
        fields = ['id', 'name']


class RugCornerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugCorner
        fields = ['id', 'name', 'image']


class RugBorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugBorder
        fields = ['id', 'name', 'image']


class RugYarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = YarnType
        fields = ['id', 'name']


class RugBackgroundSerializer(serializers.ModelSerializer):
    rug_types = serializers.SerializerMethodField()

    class Meta:
        model = RugBackground
        fields = ['id', 'name', 'image']

    # def get_rug_types(self, obj):
    #     type_names = []
    #     for rug_type in obj.rug_types.all():
    #         type_names.append(rug_type.name)
    #     return type_names


class RugTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugTile
        fields = ['id', 'name', 'image']


class RugToranjSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugToranj
        fields = ['id', 'name', 'image']


class UserRugSerializer(serializers.ModelSerializer):
    rug_type = serializers.SerializerMethodField()
    border = serializers.SerializerMethodField()
    corner = serializers.SerializerMethodField()
    background = serializers.SerializerMethodField()
    tile = serializers.SerializerMethodField()
    toranj = serializers.SerializerMethodField()

    class Meta:
        model = UserRug
        fields = ['id', 'user', 'rug_type', 'border', 'corner', 'background', 'toranj', 'tile', 'created']

    def get_rug_type(self, obj):
        try:
            return obj.rug_type.name
        except:
            return ""

    def get_border(self, obj):
        try:
            return RugBorderSerializer(obj.border).data
        except:
            return ""

    def get_corner(self, obj):
        try:
            return RugCornerSerializer(obj.corner).data
        except:
            return ""

    def get_tile(self, obj):
        try:
            return RugTileSerializer(obj.tile).data
        except:
            return ""

    def get_background(self, obj):
        try:
            return RugBackgroundSerializer(obj.background).data
        except:
            return ""

    def get_toranj(self, obj):
        try:
            return RugToranjSerializer(obj.toranj).data
        except:
            return ""


class RugLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugLog
        fields = ['rug_type', 'parts']


class RugPartTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugPartType
        fields = ['id', 'name']


class RugPartSerializer(serializers.ModelSerializer):
    part_type = RugPartTypeSerializer()
    # rug_types = serializers.SerializerMethodField()
    brand = ManufacturerSerializer()
    yarn = RugYarnTypeSerializer()
    color = ColorSerializer()
    colors = ColorSerializer(many=True)

    class Meta:
        model = RugPart
        fields = ['id', 'name', 'image', 'part_type', 'density', 'shaneh', 'brand', 'yarn', 'color',
                  'colors', 'coloring_code']

    # def get_rug_types(self, obj):
    #     type_names = []
    #     for rug_type in obj.rug_types.all():
    #         type_names.append(rug_type.name)
    #     return type_names


class RugFinderSerializer(serializers.ModelSerializer):
    similarity = serializers.SerializerMethodField()
    rug_type = serializers.SerializerMethodField()
    border = RugPartSerializer()
    corner = RugPartSerializer()
    background = RugPartSerializer()
    tile = RugPartSerializer()
    toranj = RugPartSerializer()
    yarn = RugYarnTypeSerializer()
    knot = RugPartSerializer()

    class Meta:
        model = Rug
        fields = ['id', 'name', 'rug_type', 'w_density', 'l_density', 'coloring_code', 'corner', 'border', 'tile',
                  'background', 'toranj', 'yarn', 'knot', 'full_image', 'similarity']

    def get_similarity(self, obj):
        ratio = 50
        if obj.rug_type.name == "lachak-toranj":
            ratio = 25

        try:
            return obj.similarity * ratio
        except:
            return 0

    def get_rug_type(self, obj):
        try:
            return obj.rug_type.name
        except:
            return ""

    def get_border(self, obj):
        try:
            # Pass request so serializer can create the absolute url
            return RugBorderSerializer(obj.border, context={"request": self.context.get("request")}).data
        except:
            return ""

    def get_corner(self, obj):
        try:
            # Pass request so serializer can create the absolute url
            return RugCornerSerializer(obj.corner, context={"request": self.context.get("request")}).data
        except:
            return ""

    def get_tile(self, obj):
        try:
            # Pass request so serializer can create the absolute url
            return RugTileSerializer(obj.tile, context={"request": self.context.get("request")}).data
        except:
            return ""

    # def get_background(self, obj):
    #     try:
    #         # Pass request so serializer can create the absolute url
    #         return RugBackgroundSerializer(obj.background, context={"request": self.context.get("request")}).data
    #     except:
    #         return ""

    def get_toranj(self, obj):
        try:
            # Pass request so serializer can create the absolute url
            return RugToranjSerializer(obj.toranj, context={"request": self.context.get("request")}).data
        except:
            return ""

    def get_yarn(self, obj):
        try:
            return RugYarnTypeSerializer(obj.yarn).data
        except:
            return ""

    def get_knot(self, obj):
        try:
            return RugKnotTypeSerializer(obj.knot).data
        except:
            return ""


class RugSellersSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()
    rug = RugFinderSerializer()

    class Meta:
        model = SellerRug
        fields = ['id', 'seller', 'rug', 'available', 'price', 'on_sale', 'available_sizes', 'buy_url']


class RugReplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RugReplacement
        fields = ['id', 'name', 'phone', 'national_id', 'address', 'rug_url', 'file']
        read_only_fields = ['id']

    def validate_file(self, value):
        if not value:
            return None
        if value.size > 157286400:
            raise ValidationError("file is too big")
        return value


class CustomRugSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRugSize
        fields = ['id', 'height', 'width', 'name', 'price']


class CustomRugRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRugRequest
        fields = ['id', 'name', 'phone', 'national_id', 'address', 'size', 'image']
        read_only_fields = ['id']

    def validate_image(self, value):
        if not value:
            return None
        if value.size > 157286400:
            raise ValidationError("image is too big")
        return value
