from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from users.serializers import UserSerializer
from schedules.serializers import TeamSerializer
from chats.models import TeamMessages


class TeamMessagesSerializer(serializers.ModelSerializer):

    def validate_team(self, value):
        user_id = self.context['request'].user.id
        if not value.members.filter(id=user_id).exists():
            raise serializers.ValidationError(
                _('You can\'t write message to team that isn\'t include you')
            )
        return value

class TeamMessagesListSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    team = TeamSerializer()

    class Meta:
        model = TeamMessages
        fields = '__all__'
