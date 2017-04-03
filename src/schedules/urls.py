from rest_framework import routers

from schedules.views import ShiftViewSet, PeriodViewSet, UserScheduleViewSet, \
    TeamLeaderScheduleViewSet

router = routers.DefaultRouter()
router.register('shifts', ShiftViewSet, base_name='shift')
router.register('periods', PeriodViewSet, base_name='period')
router.register('user-schedule', UserScheduleViewSet, 'user-schedule')
router.register(
    'team-leader-schedule', TeamLeaderScheduleViewSet, 'team-leader-schedule'
)


urlpatterns = [] + router.urls
