from rest_framework import serializers

from core.serializers import HyperlinkedSorlImageField
from gallery.models import Photo, Album, Video


class PhotoSerializer(serializers.ModelSerializer):
    original = HyperlinkedSorlImageField(
        '1280x1024', options={'upscale': False}
    )
    thumbnail = HyperlinkedSorlImageField(
        '432x280', options={"crop": "center"},
        source='original', read_only=True
    )

    class Meta:
        model = Photo
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
