from django.db.models.signals import post_save
from django.dispatch import receiver

from badges.models import Badge
from notices.models import Notice
from users.models import ProfileComment, Profile


def create_badge(user, type):
    Badge.objects.create(user=user, type=type)


def delete_badge(user, type):
    badge = Badge.objects.filter(user=user, type=type).first()
    if badge:
        badge.delete()


def delete_all_badges(user, type):
    Badge.objects.filter(user=user, type=type).delete()


@receiver(post_save, sender=Notice)
def create_notice_badge(sender, instance, created, **kwargs):
    if created:
        create_badge(user=instance.user, type=sender._meta.model_name)


@receiver(post_save, sender=Notice)
def delete_notice_badge(sender, instance, created, **kwargs):
    if not created and instance.is_confirmed in (True, False):
        delete_badge(user=instance.user, type=sender._meta.model_name)


@receiver(post_save, sender=ProfileComment)
def create_profile_comment_badge(sender, instance, created, **kwargs):
    if created:
        create_badge(user=instance.profile.user, type=sender._meta.model_name)


@receiver(post_save, sender=Profile)
def delete_profile_comment_badge(sender, instance, **kwargs):
    delete_all_badges(user=instance.user, type=ProfileComment._meta.model_name)


