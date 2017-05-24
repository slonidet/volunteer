from rest_framework import serializers
from core.serializers import HyperlinkedSorlImageField
from core.translation_serializers import UserTranslationMixin, \
    AdminTranslationMixin
from hall_of_fame.models import HallOfFame
from hall_of_fame.translation import HallOfFameTranslationOptions
from users.models import User


class HallOfFameBaseSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='user.profile.first_name', read_only=True)
    last_name = serializers.CharField(
        source='user.profile.last_name', read_only=True)
    image = serializers.ReadOnlyField()

    class Meta:
        model = HallOfFame
        model_translation = HallOfFameTranslationOptions


class AdminHallOfFameSerializer(AdminTranslationMixin,
                                HallOfFameBaseSerializer):
    rating = serializers.IntegerField(source='user.rating', read_only=True)

    class Meta(HallOfFameBaseSerializer.Meta):
        fields = '__all__'


class HallOfFameSerializer(UserTranslationMixin, HallOfFameBaseSerializer):

    class Meta(HallOfFameBaseSerializer.Meta):
        fields = ['id', 'user', 'image', 'is_published', 'text', 'first_name',
                  'last_name', ]


class AdminUsersHallOfFameSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(
        source='profile.last_name', read_only=True
    )
    first_name = serializers.CharField(
        source='profile.first_name', read_only=True
    )
    hall_of_fame = serializers.IntegerField(
        source='hall_of_fame.id', read_only=True
    )
    is_published = serializers.BooleanField(source='hall_of_fame.is_published')
    image = HyperlinkedSorlImageField(
        '300x300', options={"crop": "center"},
        source='hall_of_fame.image', read_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'rating', 'hall_of_fame',
                  'is_published', 'image',)
