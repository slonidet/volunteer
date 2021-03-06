from rest_framework import viewsets

from news.models import News
from news.serializers import AdminNewsSerializer, NewsSerializer


class AdminNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = AdminNewsSerializer
    filter_fields = ('is_public',)


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_public=True)
    serializer_class = NewsSerializer
    permission_classes = ()
