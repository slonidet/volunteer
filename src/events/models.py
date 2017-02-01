from django.db import models
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions


class Event(models.Model):
    """
    Events model
    """
    title = models.CharField(_('заголовок'), max_length=256)
    description = models.TextField(_('описание'))
    address = models.CharField(_('адрес'), max_length=512)
    start = models.DateTimeField(_('начало мероприятия'))
    end = models.DateTimeField(_('окончание мероприятия'))
    user_count = models.PositiveSmallIntegerField(_('количество участников'))

    class Meta(MetaPermissions):
        verbose_name = _('мероприятие')
        verbose_name_plural = _('мероприятия')
        ordering = ('start', )

    def __str__(self):
        return self.title
