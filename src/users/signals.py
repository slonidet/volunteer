from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from users.models import ProfileAttachment, User


@receiver(pre_delete, sender=ProfileAttachment)
def attachment_delete(sender, instance, **kwargs):
    """ Delete attachment from file system """
    instance.photo.delete(False)


@receiver(post_save, sender=User)
def set_default_user_group(sender, instance, **kwargs):
    instance.set_default_group()
