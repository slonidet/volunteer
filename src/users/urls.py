from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet, base_name='profile')
router.register('', UserViewSet, base_name='user')


urlpatterns = [
    url(r'auth/', obtain_auth_token, name='auth'),
] + router.urls
