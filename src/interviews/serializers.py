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
