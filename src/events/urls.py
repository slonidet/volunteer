from rest_framework import routers

from events.views import EventViewSet


router = routers.DefaultRouter()
router.register('', EventViewSet, base_name='event')



urlpatterns = [] + router.urls
