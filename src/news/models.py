from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    """
    News
    """
    title = models.CharField(_('заголовок'), max_length=1024)
    body = models.TextField(_('текст'))
    date = models.DateField(_('дата публикации'), default=timezone.now)
    is_public = models.BooleanField(_('опубликовано'), default=False)
    image = models.ImageField(_('фото'), blank=True, null=True)

    class Meta:
        verbose_name = _('новость')
        verbose_name_plural = _('новости')

    def __str__(self):
        return self.title
