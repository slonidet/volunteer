import pytz

from django.db import transaction
from django.utils.timezone import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.filters import EventFilter
from events.models import Event, Participation
from events.serializers import AdminEventSerializer, EventSerializer, \
    ParticipateEventSerializer, AdminParticipationSerializer


class AdminEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = AdminEventSerializer
    filter_class = EventFilter


class AdminParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = AdminParticipationSerializer
    filter_fields = ('event', 'status',)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(
        is_public=True, end__gt=datetime.now(tz=pytz.UTC)
    )
    serializer_class = EventSerializer
    permission_classes = ()

    @detail_route(
        methods=['post'],
        permission_classes=(IsAuthenticated,),
        serializer_class=ParticipateEventSerializer,
    )
    def participate(self, request, pk=None):
        """
        Add user in event
        :param request:
        :param pk:
        :return:
        """
        user = self.request.user
        serializer = ParticipateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data['status']
        approved_roles = (
            'approved',
            'tested',
            'interviewed',
            'prepared',
            'main',
            'reserved',
        )

        if user.role not in approved_roles:
            error_msg = _('Чтобы принять участие в мероприятии, '
                          'Ваш профиль должен быть подтвержден')
            raise exceptions.PermissionDenied(error_msg)

        with transaction.atomic():
            event = Event.objects.select_for_update().get(id=pk)
            try:
                if event.type == 'forum' and status == 'volunteer':
                    if event.volunteers_count < event.volunteer_limit:
                        Participation.objects.create(
                            user=user, event=event,
                            status=Participation.STATUS_VOLUNTEER
                        )
                        event.volunteers_count = F('volunteers_count') + 1
                        event.save()
                        role = _('волонтёр')
                    else:
                        raise exceptions.NotAcceptable(
                            _('Регистрация на мероприятие окончена '
                              '(мест для волонтеров нет)')
                        )
                else:
                    if event.participants_count < event.participants_limit:
                        Participation.objects.create(
                            user=user, event=event,
                            status=Participation.STATUS_PARTICIPANT
                        )
                        event.participants_count = F('participants_count') + 1
                        event.save()
                        role = _('участник')
                    else:
                        raise exceptions.NotAcceptable(
                            _('Регистрация на мероприятие окончена '
                              '(мест для участников нет)')
                        )

                return Response(_('Вы записались на: {} как {}').format(
                    event.title, role
                ))
            except IntegrityError:
                return Response(_('Вы уже записаны на это мероприятие'))
