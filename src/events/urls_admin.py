from rest_framework import routers

from events.views import AdminEventViewSet, AdminParticipationViewSet

router = routers.DefaultRouter()
router.register('participation', AdminParticipationViewSet,
                base_name='participation')
router.register('', AdminEventViewSet, base_name='event')


urlpatterns = [] + router.urls
