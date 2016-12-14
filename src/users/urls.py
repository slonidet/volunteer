from django.conf.urls import url
from rest_framework import routers

from users.views import (
    UserViewSet, ProfileViewSet, UserRegistrationView, AuthTokenView
)


router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet, base_name='profile')
router.register('', UserViewSet, base_name='user')


urlpatterns = [
    url(r'auth/', AuthTokenView.as_view(), name='auth'),
    url(r'registration/', UserRegistrationView.as_view(), name='registration'),
] + router.urls
