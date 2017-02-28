from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions
from users.models import User


class Notice(models.Model):
    """
    Notifications model
    """
    TYPE_CHOICES = (
        ('waiting', 'waiting'),
        ('confirmed', 'confirmed'),
        ('rejected', 'rejected'),
        ('succeed', 'succeed'),
        ('not succeed', 'not succeed'),
    )

    title = models.CharField(_('заголовок'), max_length=250)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    type = models.CharField(
        _('тип нотификации'), max_length=150, choices=TYPE_CHOICES)
    message = models.TextField(_('сообщение'))
    created_at = models.DateTimeField(_('время создания'), auto_now_add=True)
    is_confirmed = models.BooleanField(_('подтверждено'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    class Meta(MetaPermissions):
        verbose_name = _('нотификация')
        verbose_name_plural = _('нотификации')

    def __str__(self):
        return self.title
