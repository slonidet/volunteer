from rest_framework.serializers import ModelSerializer, ImageField

from chats.models import Room, Message
from core.serializers import HyperlinkedSorlImageField
from users.serializers import UserSerializer


class MessageSerializer(ModelSerializer):
    sender = UserSerializer(read_only=True)
    photo = HyperlinkedSorlImageField(
        '50x50', label='Фото', source='sender.profile_attachment.photo',
        read_only=True
    )
    thumbnail = HyperlinkedSorlImageField(
        '50x50', options={"crop": "center"},
        source='photo', read_only=True
    )

    class Meta:
        model = Message
        fields = ('room', 'text', 'timestamp', 'sender', 'photo', 'thumbnail',)


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
