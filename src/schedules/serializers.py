from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import empty

from core.nested_serializer.serializers import M2MNestedSerializerMixin
from core.serializers import ForeignKeySerializerMixin
from users.models import User, Profile
from users.serializers import BaseUserSerializer
from schedules.models import Shift, Period, Day, Place, Position, \
    UserPosition, Team


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'
        extra_kwargs = {'date': {'validators': []}}


class PeriodSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = Period
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id', 'first_name', 'last_name', 'middle_name', 'gender', 'phone'
        )


class UserSerializer(BaseUserSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')


class BaseUserPositionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = UserPosition
        fields = '__all__'


class UserSchedulePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class UserSchedulePositionSerializer(serializers.ModelSerializer):
    place = UserSchedulePlaceSerializer(read_only=True)

    class Meta:
        model = Position
        fields = '__all__'


class UserPositionSerializer(ForeignKeySerializerMixin,
                             M2MNestedSerializerMixin,
                             BaseUserPositionSerializer):
    user = UserSerializer()
    days = DaySerializer(many=True, required=False)
    position = UserSchedulePositionSerializer()

    class Meta(BaseUserPositionSerializer.Meta):
        foreign_key_fields = ('user', 'position')
        m2m_nested_fields = ('days',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'


class TeamSerializer(ForeignKeySerializerMixin, serializers.ModelSerializer):
    user_positions = BaseUserPositionSerializer(many=True, required=False)
    team_leader_position = BaseUserPositionSerializer(required=False)

    class Meta:
        model = Team
        exclude = ('members',)
        foreign_key_fields = ('team_leader_position',)

    user_position_ids = ()

    def is_valid(self, raise_exception=False):
        user_positions = self.initial_data.pop('user_positions', [])
        try:
            self.user_position_ids = [user_pos['id']
                                      for user_pos in user_positions]
        except KeyError:
            raise serializers.ValidationError(_('Нет id в структуре user'))

        return super().is_valid(raise_exception)

    def check_users_not_in_another_team(self, team=None):
        user_positions = UserPosition.objects.filter(
            id__in=self.user_position_ids, team__isnull=False
        )
        if team:
            user_positions = user_positions.exclude(team=team)

        in_another_team = user_positions.values_list('id', flat=True)
        if in_another_team:
            raise serializers.ValidationError(
                _('Пользователи с позициями {} уже распределены по командам')
                .format(','.join(in_another_team))
            )

    def create(self, validated_data):
        self.check_users_not_in_another_team()
        instance = super().create(validated_data)

        user_positions_added_to_team = UserPosition.objects.filter(
            id__in=self.user_position_ids, team__isnull=True
        )
        for user_position in user_positions_added_to_team:
            user_position.team = instance
            user_position.save()

        return instance

    def update(self, instance, validated_data):
        self.check_users_not_in_another_team(team=instance)

        user_positions_added_to_team = UserPosition.objects.filter(
            id__in=self.user_position_ids, team__isnull=True
        )
        for user_position in user_positions_added_to_team:
            user_position.team = instance
            user_position.save()

        if not self.partial:
            user_position_ids = self.user_position_ids
            user_position_ids.append(instance.team_leader_position.id)
            user_positions_removed_from_team = UserPosition.objects.filter(
                team=instance).exclude(id__in=user_position_ids)

            for user_position in user_positions_removed_from_team:
                user_position.team = None
                user_position.save()

        return super().update(instance, validated_data)


# User Schedule serializers

class TeamLeaderPositionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserPosition
        fields = ('id', 'user')


class UserScheduleTeamSerializer(serializers.ModelSerializer):
    team_leader_position = TeamLeaderPositionSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'team_leader_position')


class UserScheduleUserPositionSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    team = UserScheduleTeamSerializer(read_only=True)
    position = UserSchedulePositionSerializer(read_only=True)
    shift = ShiftSerializer(read_only=True)

    class Meta:
        model = UserPosition
        exclude = ('user',)


# Team Leader Schedule

class TeamLeaderSchedulePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class TeamLeaderScheduleTeamSerializer(serializers.ModelSerializer):
    user_positions = BaseUserPositionSerializer(many=True, read_only=True)
    place = TeamLeaderSchedulePlaceSerializer(read_only=True)

    class Meta:
        model = Team
        exclude = ('members', 'team_leader_position')


# Relevant user

class RelevantPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class RelevantProfileSerializer(ProfileSerializer):
    work_period = RelevantPeriodSerializer(read_only=True)
    work_shift = ShiftSerializer(read_only=True)

    class Meta(ProfileSerializer.Meta):
        fields = (
            'id', 'first_name', 'last_name', 'middle_name', 'phone',
            'work_period', 'work_shift', 'interesting_tourist_information',
            'interesting_transportation', 'interesting_language',
            'interesting_festival'
        )


class RelevantUserSerializer(BaseUserSerializer):
    profile = RelevantProfileSerializer(read_only=True)
    busy_days = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'profile', 'busy_days')

    def get_busy_days(self, obj):
        busy_days = Day.objects.filter(user_positions__user=obj)
        return DaySerializer(busy_days, many=True).data


# User Position Statistic

class StatisticDaySerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Day
        fields = '__all__'

    def __init__(self, instance=None, data=empty, **kwargs):
        self.day_statistics = kwargs.pop('day_statistics', None)

        super().__init__(instance, data, **kwargs)

    def get_user_count(self, obj):
        return self.day_statistics.get(obj.id, 0)


class StatisticPositionSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = Position
        exclude = ('place',)

    def get_days(self, obj):
        days = self.parent.parent.days
        statistics = self.parent.parent.statistics

        try:
            day_statistics = statistics[obj.place.id][obj.id]
        except KeyError:
            day_statistics = {}

        return StatisticDaySerializer(
            days, day_statistics=day_statistics, many=True).data


class StatisticPlaceSerializer(serializers.ModelSerializer):
    positions = StatisticPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'

    def __init__(self, instance=None, data=empty, **kwargs):
        self.days = kwargs.pop('days', None)
        self.statistics = kwargs.pop('statistics', None)

        super().__init__(instance, data, **kwargs)
