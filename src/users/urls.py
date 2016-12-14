from django.conf.urls import url
from rest_framework import routers

from users.views import (
    UserViewSet, ProfileViewSet, UserRegistrationView, AuthTokenView,
    UserActivationView)


router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet, base_name='profile')
router.register('', UserViewSet, base_name='user')


urlpatterns = [
    url(r'auth/', AuthTokenView.as_view(), name='auth'),
    url(r'registration/', UserRegistrationView.as_view(), name='registration'),
    url(r'activation/(?P<user_id>[0-9]+)/(?P<token>[a-z0-9]{32})/$',
        UserActivationView.as_view(), name='activation'),

] + router.urls
