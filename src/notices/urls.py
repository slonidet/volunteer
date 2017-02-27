from rest_framework import routers



router = routers.DefaultRouter()
# router.register('', NoticeViewSet, base_name='notices')


urlpatterns = [] + router.urls