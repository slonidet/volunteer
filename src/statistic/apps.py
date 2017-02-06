from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StatisticConfig(AppConfig):
    name = 'statistic'
    verbose_name = _('Статистика')
