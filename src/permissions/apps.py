from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PermissionsConfig(AppConfig):
    name = 'permissions'
    verbose_name = _('права доступа')