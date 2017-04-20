import django_filters
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import FilterSet

from schedules.models import UserPosition, Period, Day
from users.models import User


class UserPositionFilter(FilterSet):
    without_team = django_filters.BooleanFilter(
        label=_('Не в команде'), method='without_team_filter'
    )

    class Meta:
        model = UserPosition
        fields = (
            'position__place', 'days__period', 'shift', 'without_team',
            'position'
        )

    def without_team_filter(self, queryset, name, value):
        return queryset.filter(team__isnull=value)


class RelevantUserFilter(FilterSet):
    profile__work_period = django_filters.ModelChoiceFilter(
        queryset=Period.objects.all(), label=_('Период работы'),
        method='work_period_filter'
    )
    available_days = django_filters.ModelMultipleChoiceFilter(
        queryset=Day.objects.all(), label=_('Свободные дни'),
        method='available_days_filter'
    )

    class Meta:
        model = User
        fields = (
            'profile__work_shift', 'profile__work_period', 'username',
            'available_days', 'role'
        )

    def work_period_filter(self, queryset, name, value):
        return queryset.filter(
            Q(profile__work_period=value) |
            Q(profile__work_period__system_name=Period.ANY)
        )

    def available_days_filter(self, queryset, name, value):
        return queryset.exclude(user_positions__days__in=value)
