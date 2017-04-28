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

GROUP_LEVEL = {
    'super': 40,
    'admin': 30,
    'senior': 20,
    DEFAULT_GROUP: 10,
}
