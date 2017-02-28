from django.db.models.signals import post_save
from django.dispatch import receiver

from badges.models import Badge
from users.models import ProfileComment

SPECIAL_BADGE_TYPES = (
    ProfileComment._meta.model_name,
)
COMMON_BADGE_TYPES = [name for name, verbose in Badge.TYPE_CHOICES
                      if name not in SPECIAL_BADGE_TYPES]


@receiver(post_save)
def create_budget(sender, instance, **kwargs):
    """ Create budget if created model instance """
    if sender._meta.model_name in COMMON_BADGE_TYPES:
        Badge.objects.create(
            user=instance.user, type=sender._meta.model_name
        )


@receiver(post_save, sender=ProfileComment)
def create_profile_comment_budget(sender, instance, created, **kwargs):
    if created:
        Badge.objects.create(
            user=instance.profile.user, type=Badge._meta.model_name
        )
