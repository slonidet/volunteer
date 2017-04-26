from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HallOfFameConfig(AppConfig):
    name = 'hall_of_fame'
    verbose_name = _('доска почета')

    def ready(self):
        from hall_of_fame import signals
