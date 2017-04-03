import django_filters
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import FilterSet

from interviews.models import Interview
from users.models import User


class UserFilter(FilterSet):
    available_for_interview = django_filters.BooleanFilter(
        label=_('Доступен для интервью'),
        method='available_for_interview_filter'
    )

    class Meta:
        model = User
        fields = (
            'groups__name', 'role', 'is_active', 'available_for_interview',
            'participation__event__id', 'participation__status',
        )

    def available_for_interview_filter(self, queryset, name, value):
        if value is True:
            available_for_interview = (
                Q(interviews__isnull=True) |
                ~Q(interviews__status__in=Interview.NOT_AVAILABLE_STATUSES)
            )
            queryset = queryset.filter(available_for_interview)
        elif value is False:
            queryset = queryset.filter(
                interviews__status__in=Interview.NOT_AVAILABLE_STATUSES)

        return queryset.distinct()
