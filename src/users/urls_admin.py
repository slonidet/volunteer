from rest_framework import routers

from users import views


router = routers.DefaultRouter()
router.register('profiles', views.AdminProfileViewSet, base_name='profile')
router.register('profile-attachments', views.AdminProfileAttachmentViewSet,
                base_name='profile-attachment')
router.register('stories', views.AdminStoryViewSet, base_name='story')
router.register('', views.AdminUserViewSet, base_name='user')


urlpatterns = [] + router.urls
