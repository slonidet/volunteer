from rest_framework import viewsets, permissions

from schedules.models import Shift, Period
from schedules.serializers import ShiftSerializer, PeriodSerializer


class ShiftViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None


class PeriodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Period.objects.prefetch_related('days').all()
    serializer_class = PeriodSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
