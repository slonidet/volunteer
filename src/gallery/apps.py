from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GalleryConfig(AppConfig):
    name = 'gallery'
    verbose_name = _('галерея')

    def ready(self):
        from gallery import signals
