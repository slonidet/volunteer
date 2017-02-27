from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from badges.models import Badge
from badges.serializers import BadgeSerializer


class BadgeViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, GenericViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
