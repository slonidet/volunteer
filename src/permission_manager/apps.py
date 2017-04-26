from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PermissionManagerConfig(AppConfig):
    name = 'permission_manager'
    verbose_name = _('Управления правами')
