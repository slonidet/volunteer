from rest_framework import serializers

from notices.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        exclude = ('user', 'content_type', 'object_id')


class ArbitraryNoticeSerializer(NoticeSerializer):
    role = serializers.CharField(max_length=128)

