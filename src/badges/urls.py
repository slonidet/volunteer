from django.conf.urls import url
from rest_framework import routers

from badges.views import BadgeViewSet, BadgeTypeView

router = routers.DefaultRouter()
router.register('', BadgeViewSet, base_name='badge')


urlpatterns = [
    url(r'types/$', BadgeTypeView.as_view(), name='types'),
] + router.urls
