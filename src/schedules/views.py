from rest_framework import viewsets, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from schedules.filters import UserPositionFilter, RelevantUserFilter
from schedules.models import Shift, Period, Place, Team, UserPosition, Day
from schedules.serializers import ShiftSerializer, PeriodSerializer, \
    PlaceSerializer, TeamSerializer, UserPositionSerializer, \
    UserScheduleUserPositionSerializer, TeamLeaderScheduleTeamSerializer, \
    RelevantUserSerializer, StatisticPlaceSerializer
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
    queryset = Place.objects.prefetch_related('positions').all()
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
    filter_fields = ('place', 'shift', 'period')


class AdminUserPositionViewSet(viewsets.ModelViewSet):
    queryset = UserPosition.objects.select_related(
        'user__profile', 'position__place'
    ).prefetch_related('days', 'user__user_positions__days').distinct()
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


class AdminRelevantUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related(
        'profile__work_period', 'profile__work_shift'
    ).prefetch_related('user_positions__days').filter(
        is_active=True, role__in=(User.ROLE_MAIN_TEAM, User.ROLE_RESERVED)
    )
    serializer_class = RelevantUserSerializer
    filter_class = RelevantUserFilter
    ordering_fields = (
        'role', 'profile__work_period__system_name',
        'profile__interesting_tourist_information',
        'profile__interesting_transportation', 'profile__interesting_language',
        'profile__interesting_festival'
    )


class AdminUserPositionStatisticView(GenericAPIView):
    queryset = UserPosition.objects.prefetch_related('days').select_related(
        'position__place').all()
    serializer_class = StatisticPlaceSerializer
    filter_fields = ['shift', 'days__period', 'position__place__name']

    def get(self, request, *args, **kwargs):
        places = self.get_places_queryset()

        serializer_params = self.get_serializer_params()
        page = self.paginate_queryset(places)
        if page is not None:
            serializer = self.get_serializer(
                page, **serializer_params)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            places, **serializer_params)

        return Response(serializer.data)

    def get_places_queryset(self):
        places = Place.objects.prefetch_related('positions')
        name = self.request.query_params.get('position__place__name', None)
        if name:
            places = places.filter(name__icontains=name)
        if 'position__place__name' in self.filter_fields:
            self.filter_fields.remove('position__place__name')
        return places

    def get_serializer_params(self):
        return dict(
            days=self.get_days_context(),
            statistics=self.get_user_statistics_context(),
            many=True
        )

    def get_days_context(self):
        days = Day.objects.all()
        period = self.request.query_params.get('days__period', None)
        if period:
            days = days.filter(period=self.request.query_params['days__period'])
        return days

    def get_user_statistics_context(self):
        user_positions = self.filter_queryset(self.get_queryset()).distinct()
        if 'position__place__name' not in self.filter_fields:
            self.filter_fields.append('position__place__name')
        user_statistics = self.get_user_statistics(user_positions)
        return user_statistics

    @staticmethod
    def get_user_statistics(user_positions):
        """
        User statistic per day. Return dict structure
        {
            place_id: {
                position_id: {
                    date_id: 5,
                    ...
                },
                ...
            } ,
            ...
        }
        :param user_positions: UserPosition queryset
        :return: 
        """
        statistics = {}

        for user_position in user_positions:
            for day in user_position.days.all():
                try:
                    position = user_position.position
                    statistics[position.place.id][position.id][day.id] += 1

                except KeyError:
                    if position.place.id not in statistics:
                        statistics[position.place.id] = {}

                    if position.id not in statistics[position.place.id]:
                        statistics[position.place.id][position.id] = {}

                    if day.id not in statistics[position.place.id][position.id]:
                        statistics[position.place.id][position.id][day.id] = 1

        return statistics
