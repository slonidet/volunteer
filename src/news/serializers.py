from rest_framework import serializers

from core.serializers import HyperlinkedSorlImageField
from core.translation_serializers import AdminTranslationMixin, \
    UserTranslationMixin
from news.models import News
from news.translation import NewsTranslationOptions


class BaseNewsSerializer(serializers.ModelSerializer):
    image = HyperlinkedSorlImageField(
        '600x400', options={'upscale': False}
    )
    thumbnail = HyperlinkedSorlImageField(
        '320x240', options={"crop": "center"},
        source='image', read_only=True
    )

    class Meta:
        model = News
        model_translation = NewsTranslationOptions


class AdminNewsSerializer(AdminTranslationMixin, BaseNewsSerializer):
    class Meta(BaseNewsSerializer.Meta):
        fields = '__all__'


class NewsSerializer(UserTranslationMixin, BaseNewsSerializer):
    class Meta(BaseNewsSerializer.Meta):
        exclude = ('is_public', )
