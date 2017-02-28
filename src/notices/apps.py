from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NoticesConfig(AppConfig):
    name = 'notices'
    verbose_name = _('нотификации')
