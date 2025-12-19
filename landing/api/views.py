from rest_framework import generics
from .serializers import ContentCategorySerializer
from landing.models import ContentCategory


class ContentListAPI(generics.ListAPIView):
    serializer_class = ContentCategorySerializer
    queryset = ContentCategory.objects.all()
