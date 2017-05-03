from django.db import OperationalError
from django.db.models import F
from django.db.models.signals import post_delete
from django.dispatch import receiver

from events.models import Participation, Event


@receiver(post_delete, sender=Participation)
def decrease_event_users_counter(sender, instance, **kwargs):
    try:
        event = Event.objects.get(id=instance.event_id)
    except Event.DoesNotExist:
        return

    try:
        if instance.status == Participation.STATUS_VOLUNTEER:
            event.volunteers_count = F('volunteers_count') - 1
            event.save()
        if instance.status == Participation.STATUS_PARTICIPANT:
            event.participants_count = F('participants_count') - 1
            event.save()

    except OperationalError:
        pass
