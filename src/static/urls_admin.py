from rest_framework import routers

from static.views import AdminPageViewSet

router = routers.DefaultRouter()
router.register('static-pages', AdminPageViewSet, base_name='page')

urlpatterns = [] + router.urls
