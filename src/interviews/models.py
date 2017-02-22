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
        ('09-10', _('09-10')),
        ('10-11', _('10-11')),
        ('11-12', _('11-12')),
        ('12-13', _('12-13')),
        ('13-14', _('13-14')),
        ('14-15', _('14-15')),
        ('15-16', _('15-16')),
        ('16-17', _('16-17')),
        ('17-18', _('17-18')),
    )
    STATUS_CHOICES = (
        ('wait', _('Ожидает подтверждения')),
        ('reject', _('Волонтер отказался')),
        ('confirm', _('Волонтер согласился')),
        ('happen', _('Состоялось')),
        ('cancel', _('Не состоялось')),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Пользователь')
    )
    interviewer = models.ForeignKey(
        Interviewer, on_delete=models.CASCADE, related_name='interviews',
        verbose_name=_('Интервьюер')
    )
    date = models.DateField(_('Дата'))
    period = models.CharField(_('Время интервью'), choices=PERIOD_CHOICES,
                              max_length=5)
    status = models.CharField(_('Статус'), choices=STATUS_CHOICES,
                              max_length=8)

    class Meta(MetaPermissions):
        verbose_name = _('Интервью')
        verbose_name_plural = _('Интервью')

    def __str__(self):
        return '{0} {1}'.format(self.date, self.get_period_display())
