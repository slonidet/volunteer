from django.db import models
from django.utils.translation import ugettext_lazy as _


class Page(models.Model):
    title = models.CharField(_('заголовок'), max_length=512)
    body = models.TextField(_('тело страницы'))
