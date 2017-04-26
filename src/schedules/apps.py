from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SchedulesConfig(AppConfig):
    name = 'schedules'
    verbose_name = _('Расписание')

    def ready(self):
        from schedules import signals
