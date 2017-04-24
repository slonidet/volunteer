from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User


class HallOfFame(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='hall_of_fame',
        verbose_name=_('Пользователь')
    )
    text = models.TextField(_('Текст'))
    is_published = models.BooleanField(_('Опубликованно'), default=False)

    class Meta:
        verbose_name = _('Запись в доске почета')
        verbose_name_plural = _('Записи в доске почета')

    def __str__(self):
        return str(self.user.username)
