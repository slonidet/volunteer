from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from events.models import Event
from notices.models import Notice
from permissions.models import MetaPermissions
from users.models import User, ProfileComment, StoryComment


class Badge(models.Model):
    TYPE_CHOICES = (
        (Notice._meta.model_name, Notice._meta.verbose_name),
        (ProfileComment._meta.model_name, ProfileComment._meta.verbose_name),
        (StoryComment._meta.model_name, StoryComment._meta.verbose_name),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='badges',
        verbose_name=_('Пользователь')
    )
    type = models.CharField(_('тип'), max_length=32, choices=TYPE_CHOICES)

    class Meta(MetaPermissions):
        verbose_name = _('Баджет')
        verbose_name_plural = _('Баджеты')

    def __str__(self):
        return str(self.id)
