from rest_framework import routers

from schedules.views import AdminPlaceViewSet, AdminTeamViewSet, \
    AdminUserPositionViewSet, RelevantUserViewSet

router = routers.DefaultRouter()
router.register('places', AdminPlaceViewSet, base_name='place')
router.register('teams', AdminTeamViewSet, base_name='team')
router.register('user-positions', AdminUserPositionViewSet, 'user-position')
router.register('relevant-users', RelevantUserViewSet, 'relevant-user')


urlpatterns = [] + router.urls
