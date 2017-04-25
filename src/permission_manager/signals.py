from django.db.models.signals import post_migrate
from django.dispatch import receiver

from permission_manager.manager import set_permissions

from users.models import User, Profile

@receiver(post_migrate, sender=User)
def call_set_permissions_users(sender, **kwargs):
    set_permissions()

@receiver(post_migrate, sender=Profile)
def call_set_permissions_profiles(sender, **kwargs):
    set_permissions()
