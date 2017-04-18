from rest_framework import routers

from hall_of_fame.views import AdminHallOfFameViewSet


router = routers.DefaultRouter()
router.register('', AdminHallOfFameViewSet, base_name='hall_of_fame')


urlpatterns = [] + router.urls
