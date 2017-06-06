from rest_framework import routers

from chats.views import RoomViewSet

router = routers.DefaultRouter()
router.register('rooms', RoomViewSet, base_name='rooms')


urlpatterns = [] + router.urls
