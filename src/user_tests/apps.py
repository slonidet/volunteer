from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserTestsConfig(AppConfig):
    name = 'user_tests'
    verbose_name = _('Тесты')

