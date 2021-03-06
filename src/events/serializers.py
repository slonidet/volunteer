from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.translation_serializers import AdminTranslationMixin, \
    UserTranslationMixin
from events.models import Event, Participation
from events.translation import EventTranslationOptions


class BaseEventSerializer(serializers.ModelSerializer):
    participants_cnt = serializers.IntegerField(read_only=True)
    volunteers_cnt = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        model_translation = EventTranslationOptions

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError(
                _('Мероприятие не может закончиться раньше чем начнётся')
            )

        return data


class AdminEventSerializer(AdminTranslationMixin, BaseEventSerializer):
    volunteers = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta(BaseEventSerializer.Meta):
        exclude = ('users',)

    def get_volunteers(self, obj):
        users = obj.users.filter(
            participation__status=Participation.STATUS_VOLUNTEER
        ).values('username')

        return users

    def get_participants(self, obj):
        users = obj.users.filter(
            participation__status=Participation.STATUS_PARTICIPANT
        ).values('username')

        return users


class AdminParticipationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.profile.first_name', read_only=True
    )
    last_name = serializers.CharField(
        source='user.profile.last_name', read_only=True
    )

    class Meta:
        model = Participation
        fields = '__all__'


class EventSerializer(UserTranslationMixin, BaseEventSerializer):
    status = serializers.SerializerMethodField()

    class Meta(BaseEventSerializer.Meta):
        exclude = ('is_public', 'users',)

    def get_status(self, obj):
        try:
            participation = obj.participation.get(
                event=obj, user=self.context['request'].user
            )
            return participation.status

        except (ObjectDoesNotExist, TypeError):
            return None


class ParticipateEventSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Participation.STATUS_CHOICES)
