from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.translation_serializers import AdminTranslationMixin, \
    UserTranslationMixin
from events.models import Event
from events.translation import EventTranslationOptions


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
    class Meta(BaseEventSerializer.Meta):
        fields = '__all__'


class EventSerializer(UserTranslationMixin, BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        exclude = ('is_public',)
