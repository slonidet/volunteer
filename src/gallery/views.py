from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from core.nested_serializer.views import ReloadOnUpdateMixin
from gallery.models import Photo, Album, Video
from gallery.serializers import PhotoSerializer, AlbumSerializer, \
    VideoSerializer


class AdminPhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_fields = ('album', )


class AdminAlbumViewSet(ReloadOnUpdateMixin, ModelViewSet):
    queryset = Album.objects.prefetch_related('photos').all()
    serializer_class = AlbumSerializer


class AdminVideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class PhotoViewSet(ReadOnlyModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_fields = ('album',)
    permission_classes = ()


class AlbumViewSet(ReadOnlyModelViewSet):
    queryset = Album.objects.prefetch_related('photos').all()
    serializer_class = AlbumSerializer
    permission_classes = ()


class VideoViewSet(ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = ()
