import os

from django.db import models
from django.utils.translation import ugettext_lazy as _


def album_dir(instance, filename):
    return 'gallery/{album_id}/{filename}'.format(
        album_id=instance.album_id,
        filename=filename,
    )


class Photo(models.Model):
    """
    Photo about events
    """
    album = models.ForeignKey(
        'Album', verbose_name=_('альбом'), related_name='photos'
    )
    original = models.ImageField(_('фото'), upload_to=album_dir)
    order = models.PositiveSmallIntegerField(
        _('порядок сортировки'), blank=True, null=True
    )
    date = models.DateField(_('дата'), auto_now_add=True)

    class Meta:
        verbose_name = _('фото')
        verbose_name_plural = _('фото')
        unique_together = ('album', 'order')

    def __str__(self):
        return os.path.basename(self.original.name)


class Album(models.Model):
    """
    Photo albums
    """
    name = models.CharField(_('имя'), max_length=128)
    date = models.DateField(_('дата'), auto_now_add=True)
    order = models.PositiveSmallIntegerField(
        _('порядок сортировки'), blank=True, null=True, unique=True
    )

    class Meta:
        verbose_name = _('альбом')
        verbose_name_plural = _('альбомы')

    def __str__(self):
        return self.name


class Video(models.Model):
    """
    Links to youtube videos
    """
    description = models.CharField(_('имя'), max_length=128)
    url = models.URLField(_('url'))
    order = models.PositiveSmallIntegerField(
        _('порядок сортировки'), blank=True, null=True, unique=True
    )
    date = models.DateField(_('дата'), auto_now_add=True)

    class Meta:
        verbose_name = _('видео')
        verbose_name_plural = _('видео')

    def __str__(self):
        return self.description
