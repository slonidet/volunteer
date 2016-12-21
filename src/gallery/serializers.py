from rest_framework import serializers

from core.serializers import HyperlinkedSorlImageField
from gallery.models import Photo, Album, Video


class PhotoSerializer(serializers.ModelSerializer):
    thumb = HyperlinkedSorlImageField(
        '128x128', options={"crop": "center"}, source='origin', read_only=True
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
