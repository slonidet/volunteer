from django.conf.urls import url
from rest_framework import routers

from users import views


router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet, base_name='profile')
router.register('profile-attachments', views.ProfileAttachmentViewSet,
                base_name='profile-attachment')
router.register('', views.UserViewSet, base_name='user')


urlpatterns = [
    url(r'auth/$', views.AuthTokenView.as_view(), name='auth'),
    url(r'registration/$', views.UserRegistrationView.as_view(),
        name='registration'),
    url(r'activation/(?P<user_id>[0-9]+)/(?P<token>[a-z0-9]{32})/$',
        views.UserActivationView.as_view(), name='activation'),

] + router.urls
