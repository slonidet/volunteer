from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ChatsConfig(AppConfig):
    name = 'chats'
    verbose_name = _('Чаты')

    def ready(self):
        from chats import signals
