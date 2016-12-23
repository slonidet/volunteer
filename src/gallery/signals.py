from django.db.models.signals import pre_delete
from django.dispatch import receiver

from gallery.models import Photo


@receiver(pre_delete, sender=Photo)
def attachment_delete(sender, instance, **kwargs):
    """ Delete attachment from file system """
    instance.original.delete(False)
