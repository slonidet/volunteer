from django.db.models import F
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from events.models import Participation


@receiver(pre_delete, sender=Participation)
def decrease_event_users_counter(sender, instance, **kwargs):
    event = instance.event
    if instance.status == Participation.STATUS_VOLUNTEER:
        event.volunteers_count = F('volunteers_count') - 1
        event.save()
    if instance.status == Participation.STATUS_PARTICIPANT:
        event.participants_count = F('participants_count') - 1
        event.save()
