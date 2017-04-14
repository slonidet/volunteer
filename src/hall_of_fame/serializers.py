from rest_framework import serializers
from core.serializers import HyperlinkedSorlImageField
from core.translation_serializers import UserTranslationMixin, \
    AdminTranslationMixin
from hall_of_fame.models import HallOfFame
from hall_of_fame.translation import HallOfFameTranslationOptions


class HallOfFameBaseSerializer(serializers.ModelSerializer):
    image = HyperlinkedSorlImageField(
        '300x300', options={"crop": "center"},
        source='user.profile.story.image', read_only=True
    )
    first_name = serializers.CharField(source='user.profile.first_name')
    last_name = serializers.CharField(source='user.profile.last_name')

    class Meta:
        model = HallOfFame
        model_translation = HallOfFameTranslationOptions


class AdminHallOfFameSerializer(HallOfFameBaseSerializer,
                                AdminTranslationMixin):
    rating = serializers.IntegerField(source='user.rating')

    class Meta(HallOfFameBaseSerializer.Meta):
        fields = '__all__'


class HallOfFameSerializer(HallOfFameBaseSerializer, UserTranslationMixin):

    class Meta(HallOfFameBaseSerializer.Meta):
        fields = ['id', 'user', 'image', 'is_published', 'text', 'first_name',
                  'last_name', ]
