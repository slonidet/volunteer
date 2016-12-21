from rest_framework.serializers import ModelSerializer

from gallery.models import Photo, Album, Video


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class AlbumSerializer(ModelSerializer):
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = '__all__'


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
