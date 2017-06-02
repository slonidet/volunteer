from rest_framework.serializers import ModelSerializer

from chats.models import Room, Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
