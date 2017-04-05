from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import ForeignKeySerializerMixin
from interviews.models import Interviewer, Interview
from users.serializers import SimpleUserSerializer


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = '__all__'


class InterviewSerializer(ForeignKeySerializerMixin, ModelSerializer):
    interviewer = InterviewerSerializer()
    volunteer = SimpleUserSerializer()

    class Meta:
        model = Interview
        fields = '__all__'
        foreign_key_fields = ('interviewer', 'volunteer')

    def create(self, validated_data):
        user_not_available_for_interview = Interview.objects.filter(
            status__in=Interview.NOT_AVAILABLE_STATUSES,
            volunteer=self.initial_data['volunteer'].get('id')
        ).exists()

        if user_not_available_for_interview:
            raise serializers.ValidationError(
                _('Этот пользователь уже прилашён на интервью'))

        return super().create(validated_data)
