from django.db import models
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions


class Page(models.Model):
    title = models.CharField(_('заголовок'), max_length=512)
    body = models.TextField(_('тело страницы'))
    slug = models.SlugField(_('заголовок в URL'), max_length=128, null=True)

    class Meta(MetaPermissions):
        verbose_name = _('статическая страница')
        verbose_name_plural = _('статические страницы')

    def __str__(self):
        return self.title
