from rest_framework import routers

from hall_of_fame.views import AdminHallOfFameViewSet, \
    AdminUsersHallOfFameViewSet

router = routers.DefaultRouter()
router.register('detail', AdminHallOfFameViewSet, base_name='user_hall_of_fame')
router.register('', AdminUsersHallOfFameViewSet, base_name='hall_of_fame')


urlpatterns = [] + router.urls
