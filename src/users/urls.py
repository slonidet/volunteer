from django.conf.urls import url
from rest_framework import routers

from users.views import StoryViewSet, ResetPasswordView

router = routers.DefaultRouter()
router.register('stories', StoryViewSet, base_name='story')
# router.register('reset-password', ResetPasswordViewSet, base_name='reset')
# router.register('tests', UserTestViewSet, base_name='test')


urlpatterns = [
    url(r'^reset-password$', ResetPasswordView.as_view(),
        name='reset-password'),
] + router.urls
