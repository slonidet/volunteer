from rest_framework import viewsets, permissions

from schedules.models import Shift, Period, Place, Team, UserPosition
from schedules.serializers import ShiftSerializer, PeriodSerializer, \
    PlaceSerializer, TeamSerializer, UserPositionSerializer, \
    UserScheduleUserPositionSerializer


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
        'positions__user_positions__days', 'positions__user_positions__user',
        'positions__user_positions__user__profile'
    ).all()
    serializer_class = PlaceSerializer
    filter_fields = (
        'id', 'positions', 'positions__functionality',
        'positions__user_positions__shift',
        'positions__user_positions__days__period'
    )


class AdminTeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.select_related(
        'team_leader_position__user__profile'
    ).prefetch_related(
        'user_positions', 'user_positions__days', 'user_positions__user'
    ).all()
    serializer_class = TeamSerializer


class AdminUserPositionViewSet(viewsets.ModelViewSet):
    queryset = UserPosition.objects.select_related('user__profile')\
        .prefetch_related('days').all()
    serializer_class = UserPositionSerializer


class UserScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserPosition.objects.select_related(
        'position__place', 'shift', 'team__team_leader_position__user__profile'
    ).prefetch_related('days').all()
    serializer_class = UserScheduleUserPositionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
