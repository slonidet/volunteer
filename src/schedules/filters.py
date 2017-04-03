import django_filters
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import FilterSet

from schedules.models import UserPosition


class UserPositionFilter(FilterSet):
    without_team = django_filters.BooleanFilter(
        label=_('Не в команде'), method='without_team_filter'
    )

    class Meta:
        model = UserPosition
        fields = ('position__place', 'days__period', 'shift', 'without_team')

    def without_team_filter(self, queryset, name, value):
        return queryset.filter(team__isnull=value)
