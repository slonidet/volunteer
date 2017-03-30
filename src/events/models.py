import pytz
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import datetime

from permissions.models import MetaPermissions
from users.models import Profile, User


class Event(models.Model):
    """
    Events model
    """
    EVENT = 'event'
    FORUM = 'forum'
    EDUCATIONAL = 'educational'
    TYPE_CHOICES = (
        (EVENT, _('событие')),
        (FORUM, _('форум')),
        (EDUCATIONAL, _('образование')),)

    title = models.CharField(_('заголовок'), max_length=256)
    type = models.CharField(_('тип мероприятия'), choices=TYPE_CHOICES,
                            max_length=16)
    description = models.TextField(_('описание'))
    address = models.CharField(_('адрес'), max_length=512)
    start = models.DateTimeField(_('начало мероприятия'))
    end = models.DateTimeField(_('окончание мероприятия'))
    participants_limit = models.PositiveSmallIntegerField(
        _('максимальное количество участников'), default=0
    )
    volunteer_limit = models.PositiveSmallIntegerField(
        _('максимальное количество волонтеров'), default=0
    )
    participants_count = models.PositiveSmallIntegerField(
        _('количество записавшихся участников'), default=0
    )
    volunteers_count = models.PositiveSmallIntegerField(
        _('количество записавшихся волонтеров'), default=0
    )
    users = models.ManyToManyField(
        User, _('участники'), through='Participation')
    is_public = models.BooleanField(_('опубликовано'), default=True)

    class Meta(MetaPermissions):
        verbose_name = _('мероприятие')
        verbose_name_plural = _('мероприятия')
        ordering = ('start', )

    def __str__(self):
        return self.title

    @property
    def is_actual(self):
        return self.start > datetime.now(tz=pytz.UTC)


class Participation(models.Model):
    """
    Relational model between Event and Profile
    """
    STATUS_VOLUNTEER = 'volunteer'
    STATUS_PARTICIPANT = 'participant'
    STATUS_CHOICES = (
        (STATUS_VOLUNTEER, _('волонтёр')),
        (STATUS_PARTICIPANT, _('участник')),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(
        _('статус участника'), max_length=16, choices=STATUS_CHOICES,
        default=STATUS_PARTICIPANT
    )
    is_done = models.BooleanField(_('пользователь присутствовал'),
                                  default=False)

    class Meta(MetaPermissions):
        unique_together = (('user', 'event'),)
