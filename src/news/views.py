from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from news.models import News
from news.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_fields = ('is_public',)
    permission_classes = (DjangoModelPermissions, )


class PublicNewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_public=True)
    serializer_class = NewsSerializer
    permission_classes = ()
