from rest_framework import routers

from notices.views import NoticeViewSet


router = routers.DefaultRouter()
router.register('', NoticeViewSet, base_name='notices')


urlpatterns = [] + router.urls
