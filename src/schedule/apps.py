from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ScheduleConfig(AppConfig):
    name = 'schedule'
    verbose_name = _('Расписание')
