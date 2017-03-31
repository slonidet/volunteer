from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.translation_serializers import AdminTranslationMixin, \
    UserTranslationMixin
from events.models import Event, Participation
from events.translation import EventTranslationOptions
from users.models import User


class BaseEventSerializer(serializers.ModelSerializer):
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
        fields = '__all__'

    def get_volunteers(self, obj):
        users = User.objects.filter(
            participation__event__id=obj.id,
            participation__status=Participation.STATUS_VOLUNTEER
        ).values('username')
        return users

    def get_participants(self, obj):
        users = User.objects.filter(
            participation__event__id=obj.id,
            participation__status=Participation.STATUS_PARTICIPANT
        ).values('username')

        return users


class EventSerializer(UserTranslationMixin, BaseEventSerializer):
    status = serializers.SerializerMethodField()

    class Meta(BaseEventSerializer.Meta):
        exclude = ('is_public', 'users',)

    def get_status(self, obj):
        try:
            participation = obj.participation.get(event=obj.id)
            return participation.status
        except:
            return None


class ParticipateEventSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=16)
