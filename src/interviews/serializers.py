from rest_framework import serializers

from interviews.models import Interviewer, Interview


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = '__all__'


class InterviewSerializer(serializers.ModelSerializer):
    interviewer = InterviewerSerializer(many=True)

    class Meta:
        model = Interview
        fields = '__all__'
