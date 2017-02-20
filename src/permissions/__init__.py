"""
User permission module
"""
from django.utils.translation import ugettext_lazy as _


DEFAULT_GROUP = 'volunteer'
GROUPS = {
    'super': _('супер администратор'),
    'admin': _('администратор'),
    'senior': _('старший волонтёр'),
    DEFAULT_GROUP: _('волонтёр'),
}
