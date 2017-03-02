from rest_framework import mixins
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet

from notices.models import Notice
from notices.serializers import NoticeSerializer


class NoticeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.ListModelMixin, GenericViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
