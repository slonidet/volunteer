from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.nested_serializer.views import ReloadOnUpdateMixin
from gallery.models import Photo, Album, Video
from gallery.serializers import PhotoSerializer, AlbumSerializer, \
    VideoSerializer


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_fields = ('album', )
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )


class AlbumViewSet(ReloadOnUpdateMixin, ModelViewSet):
    queryset = Album.objects.prefetch_related('photos').all()
    serializer_class = AlbumSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
