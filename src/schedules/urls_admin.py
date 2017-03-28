from rest_framework import routers

from news.views import AdminNewsViewSet


router = routers.DefaultRouter()
router.register('', AdminNewsViewSet, base_name='news')


urlpatterns = [] + router.urls
