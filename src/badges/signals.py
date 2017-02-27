from django.db.models.signals import post_save
from django.dispatch import receiver

from badges.models import Badge
from users.models import ProfileComment


# @receiver(post_save)
# def create_budget(sender, instance, **kwargs):
#     """ Create budget if created model instance """
#     badge_types = dict(Badge.TYPE_CHOICES)
#     if sender._meta.model_name in badge_types:
#         Badge.objects.create(user=)


@receiver(post_save, sender=ProfileComment)
def create_profile_comment_budget(sender, instance, created, **kwargs):
    Badge.objects.create(user=instance.profile.user, )
