from rest_framework.serializers import ModelSerializer

from hall_of_fame.models import HallOfFame


class HallOfFameSerializer(ModelSerializer):
    class Meta:
        model = HallOfFame
        fields = '__all__'
