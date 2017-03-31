from rest_framework import routers

from schedules.views import ShiftViewSet, PeriodViewSet, UserScheduleViewSet

router = routers.DefaultRouter()
router.register('shifts', ShiftViewSet, base_name='shift')
router.register('periods', PeriodViewSet, base_name='period')
router.register('user-schedules', UserScheduleViewSet, 'user-schedule')


urlpatterns = [] + router.urls
