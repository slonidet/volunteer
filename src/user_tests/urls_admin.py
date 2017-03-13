from django.conf.urls import url
from rest_framework import routers

from user_tests.views import AdminUserTestViewSet

router = routers.DefaultRouter()
router.register('', AdminUserTestViewSet, base_name='user-answer')


urlpatterns = [] + router.urls
