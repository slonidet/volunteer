from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet

from static.models import Page
from static.serializers import PageSerializer, AdminPageSerializer


class AdminPageViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin, mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = AdminPageSerializer
    lookup_field = 'slug'


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = ()
    lookup_field = 'slug'
