from django.db import models
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions
from schedules.models import Team


class TeamMessages(models.Model):
    """
    Messages for Teams
    """
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='messages',
        verbose_name=_('Команда')
    )
    sender = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='messages',
        verbose_name=_('Отправитель')
    )
    text = models.TextField(_('Текст'))

    class Meta(MetaPermissions):
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')

    def __str__(self):
        return 'Message {id} from {sender} in {team}'.format(
            id=self.id,
            sender=self.sender,
            team=self.team
        )
