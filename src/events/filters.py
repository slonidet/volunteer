import django_filters
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import FilterSet

from events.models import Event


class EventFilter(FilterSet):
    is_actual = django_filters.BooleanFilter(
        label=_('актуально'), method='actual_filter'
    )

    class Meta:
        model = Event
        fields = ('is_public', 'is_actual')

    def actual_filter(self, queryset, name, value):
        return [i for i in queryset if i.is_actual == value]
