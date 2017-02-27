from rest_framework import routers

from badges.views import BadgeViewSet


router = routers.DefaultRouter()
router.register('', BadgeViewSet, base_name='badge')


urlpatterns = [] + router.urls
