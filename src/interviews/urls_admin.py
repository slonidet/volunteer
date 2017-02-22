from rest_framework import routers


router = routers.DefaultRouter()
# router.register('photo-album', AdminAlbumViewSet, base_name='photo-album')

urlpatterns = [] + router.urls
