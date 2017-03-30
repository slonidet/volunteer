from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from interviews.models import Interview
from user_tests.models import UserTest
from users.models import User, Profile


@receiver(post_save, sender=Profile)
def profile_rating(sender, instance, created, **kwargs):
    """
    Add 1 point to user's rating
    """
    if created:
        user = instance.user
        user.rating = F('rating') + 1
        user.save()


@receiver(post_save, sender=UserTest)
def test_rating(sender, instance, created, **kwargs):
    is_finished = instance.finished_at
    if is_finished:
        user = instance.user
        user.rating = F('rating') + 1
        user.save()


@receiver(post_save, sender=Interview)
def interview_rating(sender, instance, created, **kwargs):
    status = instance.status
    if status == Interview.STATUS_HAPPEN:
        user = instance.user
        user.rating = F('rating') + 3
        user.save()


