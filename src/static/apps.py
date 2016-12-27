from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StaticConfig(AppConfig):
    name = 'static'
    verbose_name = _('статические страницы')
