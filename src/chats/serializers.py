from rest_framework.serializers import ModelSerializer

from chats.models import Room, Message
from users.serializers import UserSerializer


class MessageSerializer(ModelSerializer):
    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ('room', 'text', 'timestamp', 'user',)


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
