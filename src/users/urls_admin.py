from rest_framework import routers

from users import views


router = routers.SimpleRouter()
router.register('profiles', views.AdminProfileViewSet, base_name='profile')
router.register('profile-attachments', views.AdminProfileAttachmentViewSet,
                base_name='profile-attachment')
router.register('stories', views.AdminStoryViewSet, base_name='story')
router.register('groups', views.AdminUserGroupViewSet, base_name='group')
router.register('', views.AdminUserViewSet, base_name='user')


urlpatterns = [] + router.urls
