from django.db import models
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions
from users.models import User


class Interviewer(models.Model):
    name = models.CharField(_('Имя'), max_length=128)

    class Meta(MetaPermissions):
        verbose_name = _('Интервьюер')
        verbose_name_plural = _('Интервьюеры')

    def __str__(self):
        return self.name


class Interview(models.Model):
    PERIOD_CHOICES = (
        (1, _('09-10')), (2, _('10-11')), (3, _('11-12')), (4, _('12-13')),
        (5, _('13-14')), (6, _('14-15')), (7, _('15-16')), (8, _('16-17')),
        (9, _('17-18')),
    )
    STATUS_CHOICES = (
        ('wait', _('Ожидает подтверждения')),
        ('reject', _('Волонтер отказался')),
        ('confirm', _('Волонтер согласился')),
        ('happen', _('Состоялось')),
        ('cancel', _('Не состоялось')),
    )

    volunteer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Пользователь')
    )
    interviewer = models.ForeignKey(
        Interviewer, on_delete=models.CASCADE, related_name='interviews',
        verbose_name=_('Интервьюер')
    )
    date = models.DateField(_('Дата'))
    period = models.PositiveSmallIntegerField(
        _('Время интервью'), choices=PERIOD_CHOICES
    )
    status = models.CharField(_('Статус'), choices=STATUS_CHOICES,
                              max_length=8, default='wait')

    class Meta(MetaPermissions):
        verbose_name = _('Интервью')
        verbose_name_plural = _('Интервью')

    def __str__(self):
        return '{0} {1}'.format(self.date, self.get_period_display())
