from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.models import ProfileAttachment


@receiver(pre_delete, sender=ProfileAttachment)
def attachment_delete(sender, instance, **kwargs):
    """ Delete attachment from file system """
    instance.photo.delete(False)
