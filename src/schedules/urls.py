from rest_framework import routers

from schedules.views import ShiftViewSet, PeriodViewSet

router = routers.DefaultRouter()
router.register('shifts', ShiftViewSet, base_name='shift')
router.register('periods', PeriodViewSet, base_name='period')


urlpatterns = [] + router.urls
