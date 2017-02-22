from rest_framework import mixins
from rest_framework.generics import DestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from badges.models import Badge
from badges.serializers import BadgeSerializer


class BadgeViewSet(mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
