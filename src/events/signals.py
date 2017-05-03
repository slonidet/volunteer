from django.db import OperationalError
from django.db.models import F
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from events.models import Participation


@receiver(pre_delete, sender=Participation)
def decrease_event_users_counter(sender, instance, **kwargs):
    event = instance.event
    participant_statuses = (
        Participation.STATUS_VOLUNTEER, Participation.STATUS_PARTICIPANT
    )

    if instance.status in participant_statuses:
        event.volunteers_count = F('{}s_count'.format(instance.status)) - 1
        try:
            event.save()
        except OperationalError:
            pass
