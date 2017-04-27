from rest_framework import routers

from notices.views import ArbitraryNoticeViewSet


router = routers.DefaultRouter()
router.register('', ArbitraryNoticeViewSet, base_name='arbitrary-notices')


urlpatterns = [] + router.urls
