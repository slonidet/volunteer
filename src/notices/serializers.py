from rest_framework import serializers

from notices.models import Notice


class NoticeSerializer(serializers.Modelserializer):
    class Meta:
        model = Notice
        fields = '__all__'
