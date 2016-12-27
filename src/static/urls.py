from rest_framework import routers

from static.views import PageViewSet


router = routers.DefaultRouter()
router.register('pages', PageViewSet, base_name='page')

urlpatterns = [] + router.urls
