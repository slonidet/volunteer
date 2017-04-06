from django.db import models
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions


class Place(models.Model):
    """
    Object of the volunteers service
    """
    name = models.CharField(_('Название объекта'), max_length=256)

    class Meta(MetaPermissions):
        verbose_name = _('Объект')
        verbose_name_plural = _('Объекты')

    def __str__(self):
        return self.name


class Position(models.Model):
    """
    Functional direction
    """
    FUNCTIONALITY_TOURIST_INFORMATION = 'tourist_information'
    FUNCTIONALITY_TRANSPORTATION = 'transportation'
    FUNCTIONALITY_LANGUAGE = 'language'
    FUNCTIONALITY_FESTIVAL = 'festival'
    FUNCTIONALITY_CHOICES = (
        (
            FUNCTIONALITY_TOURIST_INFORMATION,
            _('Информационно-туристическая функция')
        ),
        (FUNCTIONALITY_TRANSPORTATION, _('Транспортная функция')),
        (FUNCTIONALITY_LANGUAGE, _('Лингвистическая функцияфункция')),
        (FUNCTIONALITY_FESTIVAL, _('Фестиваль болельщиков')),
    )

    name = models.CharField(_('Название'), max_length=256)
    functionality = models.CharField(
        _('Функциональное направление'), choices=FUNCTIONALITY_CHOICES,
        max_length=32
    )
    place = models.ForeignKey(
        Place, related_name='positions', on_delete=models.CASCADE,
        verbose_name=_('Объект')
    )

    class Meta(MetaPermissions):
        verbose_name = _('Позиция')
        verbose_name_plural = _('Позиции')

    def __str__(self):
        return self.name


class Shift(models.Model):
    """
    Volunteer's duty shift
    """
    FIRST = 'first'
    SECOND = 'second'
    CHOICES = (
        (FIRST, _('10:00 – 16:00')),
        (SECOND, _('16:00 – 22:00')),
    )

    name = models.CharField(_('Название'), max_length=128, unique=True)
    system_name = models.CharField(
        _('Системное имя'), max_length=8, unique=True, choices=CHOICES
    )

    class Meta(MetaPermissions):
        verbose_name = _('Смена')
        verbose_name_plural = _('Смены')

    def __str__(self):
        return self.name


class Period(models.Model):
    """
    Volunteer's duty period
    """
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'
    ANY = 'any'
    CHOICES = (
        (FIRST, _('13 – 23 июня 2018 года')),
        (SECOND, _('24 июня – 4 июля 2018 года')),
        (THIRD, _('5 – 15 июля 2018 года')),
        (ANY, _('в любой указанный период')),
    )

    name = models.CharField(_('Название'), max_length=128, unique=True)
    system_name = models.CharField(
        _('Системное имя'), max_length=8, unique=True, choices=CHOICES
    )

    class Meta(MetaPermissions):
        verbose_name = _('Поток')
        verbose_name_plural = _('Потоки')

    def __str__(self):
        return self.name


class Day(models.Model):
    """
    Date of the period
    """
    period = models.ForeignKey(
        Period, related_name='days', on_delete=models.CASCADE,
        verbose_name=_('Период')
    )
    date = models.DateField(_('Дата'), unique=True)

    class Meta(MetaPermissions):
        verbose_name = _('День потока')
        verbose_name_plural = _('Дни потоков')

    def __str__(self):
        return str(self.date)


class UserPosition(models.Model):
    """
    User on positional (M2M through model)
    """
    position = models.ForeignKey(
        Position, related_name='user_positions', on_delete=models.CASCADE,
        verbose_name=_('Позиция')
    )
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, verbose_name=_('Волонтёр'),
        related_name='user_positions'
    )
    team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_('Команда'), related_name='user_positions'
    )
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT)
    days = models.ManyToManyField(
        Day, verbose_name=_('Дни потока'), related_name='user_positions'
    )
    is_permanent = models.BooleanField(_('Закреплённый'))

    class Meta(MetaPermissions):
        verbose_name = _('Позиция пользователя')
        verbose_name_plural = _('Позиции пользователя')
        unique_together = (('user', 'team'), )

    def __str__(self):
        return str(self.id)


class Team(models.Model):
    """
    User's teams for working on places
    """
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='teams',
        verbose_name=_('Объект')
    )
    team_leader_position = models.OneToOneField(
        UserPosition, on_delete=models.PROTECT,
        related_name='team_leader', verbose_name=_('Старший волонтёр'),
        limit_choices_to={'is_permanent': True}
    )
    members = models.ManyToManyField(
        'users.User', through=UserPosition, verbose_name=_('Члены команды')
    )
    shift = models.ForeignKey(
        Shift, on_delete=models.PROTECT, verbose_name=_('Смена')
    )
    period = models.ForeignKey(
        Period, on_delete=models.PROTECT, verbose_name=_('Поток')
    )

    class Meta(MetaPermissions):
        verbose_name = _('Команда')
        verbose_name_plural = _('Команды')

    def __str__(self):
        return ','.join((self.place.name, self.period.name, self.shift.name))
