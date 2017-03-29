from rest_framework import viewsets, permissions

from schedules.models import Shift, Period, Place
from schedules.serializers import ShiftSerializer, PeriodSerializer, \
    PlaceSerializer


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


class AdminPlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.prefetch_related(
        'positions', 'positions__user_positions',
        'positions__user_positions__days'
    ).all()
    serializer_class = PlaceSerializer
    filter_fields = (
        'id', 'positions', 'positions__functionality',
        'positions__user_positions__shift',
        'positions__user_positions__days__period'
    )
