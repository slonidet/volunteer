from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from hall_of_fame.models import HallOfFame
from hall_of_fame.serializers import HallOfFameSerializer, \
    AdminHallOfFameSerializer


class AdminHallOfFameViewSet(ModelViewSet):
    queryset = HallOfFame.objects.all().select_related('user__profile')
    serializer_class = AdminHallOfFameSerializer
    permission_classes = (permissions.IsAdminUser,)


class HallOfFameView(ListAPIView):
    queryset = HallOfFame.objects.filter(is_published=True)\
        .select_related('user__profile')
    serializer_class = HallOfFameSerializer
    permission_classes = ()
