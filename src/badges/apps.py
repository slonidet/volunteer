from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BadgesConfig(AppConfig):
    name = 'badges'
    verbose_name = _('Баджеты')
