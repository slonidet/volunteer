from django.db.models.signals import post_save
from django.dispatch import receiver

from schedules.models import Team


@receiver(post_save, sender=Team)
def add_team_leader_to_members(sender, instance, **kwargs):
    """ Add team leader to team members """
    team_leader_position = instance.team_leader_position
    if team_leader_position and team_leader_position.team != instance:
        team_leader_position.team = instance
        team_leader_position.save()
