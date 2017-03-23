import pytz
from django.utils.timezone import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import exceptions
from rest_framework.response import Response

from events.filters import EventFilter
from events.models import Event, Participation
from events.serializers import AdminEventSerializer, EventSerializer
from users.models import User


class AdminEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = AdminEventSerializer
    filter_class = EventFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_public=True,
                                    start__gt=datetime.now(tz=pytz.UTC))
    serializer_class = EventSerializer
    permission_classes = ()

    @detail_route(methods=['post'], permission_classes=())
    def participate(self, request, pk=None):
        """
        Add user in event
        :param request:
        :param pk:
        :return:
        """
        user = self.request.user
        event = Event.objects.get(id=pk)
        approved_roles = [
            'approved',
            'tested',
            'interviewed',
            'prepared']
        volunteer_roles = [
            'main',
            'reserved']
        approved_users = User.objects.filter(role__in=approved_roles)
        volunteers = User.objects.filter(role__in=volunteer_roles)

        if user in approved_users or volunteers and event.type == 'event':
            try:
                Participation.objects.create(
                    user=user, event=event, status='participant')
                if user in approved_users:
                    return Response(
                        _('Вы записались на: {}, как участник').format(
                            event.title))
                if user in volunteers:
                    return Response(
                        _('Вы записались на: {}, как волонтер').format(
                            event.title))
            except IntegrityError:
                error_msg = _('Вы уже записались на данное мероприятие')
                raise exceptions.PermissionDenied(error_msg)

        if user in volunteers or approved_users and event.type != 'event':
            Participation.objects.create(
                user=user, event=event, status='volunteer')
            return Response(
                _('Вы записались на: {}').format(event.title))

        else:
            error_msg = _('Чтобы принять участие в мероприятии, '
                          'Ваш профиль должен быть подтвержден')
            raise exceptions.PermissionDenied(error_msg)
