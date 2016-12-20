from django.conf.urls import url
from rest_framework import routers

from users import views


router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet, base_name='profile')
router.register('profile-attachments', views.ProfileAttachmentViewSet,
                base_name='profile-attachment')
router.register('', views.UserViewSet, base_name='user')


urlpatterns = [

] + router.urls
