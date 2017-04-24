from django.conf.urls import url
from rest_framework import routers

from schedules.views import AdminPlaceViewSet, AdminTeamViewSet, \
    AdminUserPositionViewSet, AdminRelevantUserViewSet, \
    AdminUserPositionStatisticView

router = routers.DefaultRouter()
router.register('places', AdminPlaceViewSet, base_name='place')
router.register('teams', AdminTeamViewSet, base_name='team')
router.register('user-positions', AdminUserPositionViewSet, 'user-position')
router.register('relevant-users', AdminRelevantUserViewSet, 'relevant-user')


urlpatterns = [
    url(
        r'user-position-statistics/$',
        AdminUserPositionStatisticView.as_view(),
        name='user-position-statistic'
    ),
] + router.urls
