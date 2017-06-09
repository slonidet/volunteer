from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from chats.models import Message
from chats.serializers import MessageSerializer


class ListMessagesMixin(object):
    @detail_route(
        methods=['get'], serializer_class=MessageSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def messages(self, request, pk=None):
        queryset = Message.objects.filter(room_id=pk)
        page = self.paginate_queryset(queryset)
        serializer = MessageSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
