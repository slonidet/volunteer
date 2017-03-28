from rest_framework import routers

from schedules.views import ShiftViewSet

router = routers.DefaultRouter()
router.register('shifts', ShiftViewSet, base_name='shift')


urlpatterns = [] + router.urls
