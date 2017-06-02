from rest_framework import routers

from chats.views import AdminRoomViewSet

router = routers.DefaultRouter()
router.register('rooms', AdminRoomViewSet, base_name='rooms')


urlpatterns = [] + router.urls
