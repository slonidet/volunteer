from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.serializers import HyperlinkedSorlImageField
from core.translation_serializers import UserTranslationMixin, \
    AdminTranslationMixin
from hall_of_fame.models import HallOfFame
from hall_of_fame.translation import HallOfFameTranslationOptions


class HallOfFameBaseSerializer(ModelSerializer):
    image = HyperlinkedSorlImageField(
        '300x300', options={"crop": "center"},
        source='user.profile.story.image', read_only=True
    )

    class Meta:
        model = HallOfFame
        model_translation = HallOfFameTranslationOptions


class AdminHallOfFameSerializer(HallOfFameBaseSerializer, AdminTranslationMixin):
    rating = SerializerMethodField()

    def get_rating(self, obj):
        return obj.user.rating

    class Meta(HallOfFameBaseSerializer.Meta):
        fields = '__all__'


class HallOfFameSerializer(HallOfFameBaseSerializer, UserTranslationMixin):

    class Meta(HallOfFameBaseSerializer.Meta):
        fields = ['id', 'user', 'image', 'is_published', 'text', ]
