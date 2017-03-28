from rest_framework import viewsets, permissions

from schedules.models import Shift
from schedules.serializers import ShiftSerializer


class ShiftViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
