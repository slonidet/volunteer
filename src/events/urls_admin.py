from rest_framework import routers

from events.views import AdminEventViewSet

router = routers.DefaultRouter()
router.register('', AdminEventViewSet, base_name='event')


urlpatterns = [] + router.urls
