from django.db.models.signals import post_save
from django.dispatch import receiver

from chats.models import Room
from schedules.models import Team


@receiver(post_save, sender=Team)
def create_room(sender, instance, created, **kwargs):
    team = instance
    if created:
        Room.objects.create(team=team, name=instance.__str__())
