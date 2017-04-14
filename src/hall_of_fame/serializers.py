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

    first_name = SerializerMethodField()
    last_name = SerializerMethodField()

    def get_first_name(self, obj):
        return obj.user.profile.first_name

    def get_last_name(self, obj):
        return obj.user.profile.last_name

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
        fields = ['id', 'user', 'image', 'is_published', 'text', 'first_name', 'last_name' ]
