from rest_framework import routers

from gallery.views import AlbumViewSet, PhotoViewSet, VideoViewSet

router = routers.DefaultRouter()
router.register('photo-album', AlbumViewSet, base_name='photo-album')
router.register('photo', PhotoViewSet, base_name='photo')
router.register('video', VideoViewSet, base_name='video')


urlpatterns = [] + router.urls
