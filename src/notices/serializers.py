from rest_framework import serializers

from notices.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        exclude = ('user', 'content_type', 'object_id',)


class ArbitraryNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'created_at', 'message', 'title', )
