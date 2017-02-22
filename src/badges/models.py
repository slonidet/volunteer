from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions
from users.models import User


class Badge(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='badges',
        verbose_name=_('Пользователь')
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta(MetaPermissions):
        verbose_name = _('Баджет')
        verbose_name_plural = _('Баджеты')

    def __str__(self):
        return str(self.id)
