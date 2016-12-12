from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserViewSet


router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    url(r'auth/', obtain_auth_token, name='auth'),
    # url(r'user/', UserProfileView.as_view(), name='user-profile'),
] + router.urls
