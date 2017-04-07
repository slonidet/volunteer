from rest_framework.viewsets import ModelViewSet

from hall_of_fame.models import HallOfFame
from hall_of_fame.serializers import HallOfFameSerializer


class AdminHallOfFameViewSet(ModelViewSet):
    queryset = HallOfFame.objects.all()
    serializer_class = HallOfFameSerializer
