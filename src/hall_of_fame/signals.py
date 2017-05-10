from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from interviews.models import Interview
from user_tests.models import UserTest
from events.models import Event, Participation
from users.models import Profile, User


@receiver(post_save, sender=Profile)
def profile_rating(sender, instance, created, **kwargs):
    user = instance.user
    if created or user.role == User.ROLE_APPROVED:
        user.rating = F('rating') + 1
    if not created and user.role != User.ROLE_APPROVED:
        user.rating = F('rating') - 1
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
        user = instance.volunteer
        user.rating = F('rating') + 3
        user.save()


@receiver(post_save, sender=Participation)
def event_rating(sender, instance, created, **kwargs):
    user = instance.user
    event = Event.objects.get(participation=instance.id)

    if event.type == Event.EVENT:
        if instance.is_done:
            user.rating = F('rating') + 5
        else:
            user.rating = F('rating') - 5

    if event.type == Event.EDUCATIONAL:
        if instance.is_done:
            user.rating = F('rating') + 1
        else:
            user.rating = F('rating') - 1

    if event.type == Event.FORUM:
        if instance.is_done:
            if instance.status == Participation.STATUS_PARTICIPANT:
                user.rating = F('rating') + 7
            if instance.status == Participation.STATUS_VOLUNTEER:
                user.rating = F('rating') + 10
        else:
            if instance.status == Participation.STATUS_PARTICIPANT:
                user.rating = F('rating') - 7
            if instance.status == Participation.STATUS_VOLUNTEER:
                user.rating = F('rating') - 10

    user.save()
