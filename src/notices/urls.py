from rest_framework import routers

from notices.views import NoticeViewSet, ArbitraryNoticeViewSet


router = routers.DefaultRouter()
router.register('', NoticeViewSet, base_name='notice')
router.register('',
                ArbitraryNoticeViewSet,
                base_name='arbitrary-notices')


urlpatterns = [] + router.urls
