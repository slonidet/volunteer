from rest_framework import routers

from gallery.views import AdminAlbumViewSet, AdminPhotoViewSet, AdminVideoViewSet

router = routers.DefaultRouter()
router.register('photo-album', AdminAlbumViewSet, base_name='photo-album')
router.register('photo', AdminPhotoViewSet, base_name='photo')
router.register('video', AdminVideoViewSet, base_name='video')


urlpatterns = [] + router.urls
