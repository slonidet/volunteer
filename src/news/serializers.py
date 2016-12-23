from rest_framework import serializers

from core.serializers import HyperlinkedSorlImageField
from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    image = HyperlinkedSorlImageField(
        '600x400', options={'upscale': False}
    )
    thumbnail = HyperlinkedSorlImageField(
        '320x240', options={"crop": "center"},
        source='image', read_only=True
    )

    class Meta:
        model = News
        fields = '__all__'