import pytz
from django.utils.timezone import datetime
from rest_framework import viewsets

from events.filters import EventFilter
from events.models import Event
from events.serializers import AdminEventSerializer, EventSerializer


class AdminEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = AdminEventSerializer
    filter_class = EventFilter


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(is_public=True,
                                    start__gt=datetime.now(tz=pytz.UTC))
    serializer_class = EventSerializer
    permission_classes = ()
