from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import permissions, generics
from schedules.models import Team
from chats.models import TeamMessages
from chats.serializers import TeamMessagesSerializer, \
    TeamMessagesListSerializer


class TeamMessagesView(generics.ListAPIView):
    queryset = TeamMessages.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TeamMessagesListSerializer

    def get(self, request, team_id, *args, **kwargs):
        team = get_object_or_404(Team.objects.all(), pk=int(team_id))
        if not team.members.filter(id=request.user.id).exists():
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class AdminTeamMessagesView(generics.ListAPIView):
    queryset = TeamMessages.objects.all()
    serializer_class = TeamMessagesSerializer
