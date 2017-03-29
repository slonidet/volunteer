from rest_framework import routers

from schedules.views import AdminPlaceViewSet

router = routers.DefaultRouter()
router.register('places', AdminPlaceViewSet, base_name='place')


urlpatterns = [] + router.urls
