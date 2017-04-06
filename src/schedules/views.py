from rest_framework import viewsets, permissions

from schedules.filters import UserPositionFilter, RelevantUserFilter
from schedules.models import Shift, Period, Place, Team, UserPosition
from schedules.serializers import ShiftSerializer, PeriodSerializer, \
    PlaceSerializer, TeamSerializer, UserPositionSerializer, \
    UserScheduleUserPositionSerializer, TeamLeaderScheduleTeamSerializer, \
    RelevantUserSerializer
from users.models import User


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
        'user_positions', 'user_positions__days', 'user_positions__user',
        'user_positions__user__profile'
    ).all()
    serializer_class = TeamSerializer


class AdminUserPositionViewSet(viewsets.ModelViewSet):
    queryset = UserPosition.objects.select_related('user__profile')\
        .prefetch_related('days').all()
    serializer_class = UserPositionSerializer
    filter_class = UserPositionFilter


class UserScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserPosition.objects.select_related(
        'position__place', 'shift', 'team__team_leader_position__user__profile'
    ).prefetch_related('days').all()
    serializer_class = UserScheduleUserPositionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TeamLeaderScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.prefetch_related(
        'user_positions', 'user_positions__days', 'user_positions__user',
        'user_positions__user__profile'
    ).all()
    serializer_class = TeamLeaderScheduleTeamSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(
            team_leader_position__user=self.request.user
        )


class RelevantUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related('profile__work_period')\
        .filter(
            is_active=True,
            role__in=(User.ROLE_MAIN_TEAM, User.ROLE_RESERVED)
        )
    serializer_class = RelevantUserSerializer
    filter_class = RelevantUserFilter
    ordering_fields = (
        'role', 'profile__work_period__system_name',
        'profile__interesting_tourist_information',
        'profile__interesting_transportation', 'profile__interesting_language',
        'profile__interesting_festival'
    )
