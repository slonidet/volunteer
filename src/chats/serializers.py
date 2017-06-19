from rest_framework.serializers import ModelSerializer

from chats.models import Room, Message
from users.serializers import UserSerializer


class MessageSerializer(ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('room', 'text', 'timestamp', 'sender', )


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
