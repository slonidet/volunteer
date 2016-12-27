from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet

from static.models import Page
from static.serializers import PageSerializer


class AdminPageViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin, mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = ()
