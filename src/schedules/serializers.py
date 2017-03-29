from rest_framework import serializers

from schedules.models import Shift, Period, Day, Place, Position, UserPosition


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = Period
        fields = '__all__'


class UserPositionSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = UserPosition
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    user_positions = UserPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Position
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'
