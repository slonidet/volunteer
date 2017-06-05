from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from chats.mixins import ListMessagesMixin
from chats.models import Room
from chats.serializers import RoomSerializer


class AdminRoomViewSet(ModelViewSet, ListMessagesMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAdminUser,)


class RoomViewSet(ReadOnlyModelViewSet, ListMessagesMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)
