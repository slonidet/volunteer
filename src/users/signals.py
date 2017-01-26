from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from users.models import ProfileAttachment, Profile, User


@receiver(pre_delete, sender=ProfileAttachment)
def attachment_delete(sender, instance, **kwargs):
    """ Delete attachment from file system """
    instance.photo.delete(False)


@receiver(post_save, sender=Profile)
def set_candidate_role_profile(sender, instance, created, **kwargs):
    """ Set user role as candidate if fill profile """
    if created:
        _set_candidate_role(instance, 'profile_attachment')


@receiver(post_save, sender=ProfileAttachment)
def set_candidate_role_attachment(sender, instance, created, **kwargs):
    """ Set user role as candidate if exist profile attachment """
    if created:
        _set_candidate_role(instance, 'profile')


def _set_candidate_role(instance, checked_model_field):
    user = instance.user
    if hasattr(user, checked_model_field):
        user.role = User.ROLE_CANDIDATE
        user.save()
