from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions
from schedules.models import Team
from users.models import User


class Room(models.Model):
    """
    Team's Room
    """
    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name='room',
        verbose_name=_('Команда')
    )
    is_active = models.BooleanField(_('чат запущен'), default=True)
    name = models.CharField(_('имя'), max_length=200, default='default')

    class Meta(MetaPermissions):
        verbose_name = _('Комната')
        verbose_name_plural = _('Комнаты')

    def __str__(self):
        return ','.join((
            self.team.place.name, self.team.period.name, self.team.shift.name))


class Message(models.Model):
    """
    Messages for Rooms
    """
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='messages',
        verbose_name=_('Команда')
    )
    sender = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='messages',
        verbose_name=_('Отправитель')
    )
    text = models.TextField(_('Текст'))
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta(MetaPermissions):
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')
        ordering = ['-timestamp', ]

    def __str__(self):
        return str(self.id)
