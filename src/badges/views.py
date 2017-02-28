from rest_framework import mixins, permissions, views
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from badges.models import Badge
from badges.serializers import BadgeSerializer


class BadgeViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, GenericViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class BadgeTypeView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(dict(Badge.TYPE_CHOICES))

