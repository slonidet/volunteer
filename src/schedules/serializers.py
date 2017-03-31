from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

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
            'id', 'status', 'first_name', 'last_name', 'middle_name', 'gender',
            'phone'
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


class UserPositionSerializer(ForeignKeySerializerMixin,
                             M2MNestedSerializerMixin,
                             BaseUserPositionSerializer):
    user = UserSerializer()
    days = DaySerializer(many=True, required=False)

    class Meta(BaseUserPositionSerializer.Meta):
        foreign_key_fields = ('user',)
        m2m_nested_fields = ('days',)


class PositionSerializer(serializers.ModelSerializer):
    user_positions = UserPositionSerializer(many=True, read_only=True)

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


class SimpleTeamSerializer(TeamSerializer):
    class Meta:
        model = Team
        fields = ('id', 'team_leader_position')


class UserScheduleUserPositionSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    team = SimpleTeamSerializer(read_only=True)

    class Meta:
        model = UserPosition
        exclude = ('user',)


class UserSchedulePositionSerializer(PositionSerializer):
    user_positions = UserScheduleUserPositionSerializer(
        many=True, read_only=True
    )


class UserSchedulePlaceSerializer(PlaceSerializer):
    positions = UserSchedulePositionSerializer(many=True, read_only=True)

