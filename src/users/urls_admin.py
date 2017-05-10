from rest_framework import routers

from users.views import AdminProfileViewSet, AdminProfileAttachmentViewSet, \
    AdminStoryViewSet, AdminStoryCommentViewSet, AdminUserGroupViewSet, \
    AdminUserViewSet, AdminProfileCityProfessionSearch, AdminEquipmentViewSet

router = routers.DefaultRouter()
router.register('profiles', AdminProfileViewSet, base_name='profile')
router.register('profile-attachments', AdminProfileAttachmentViewSet,
                base_name='profile-attachment')
router.register('stories', AdminStoryViewSet, base_name='story')
router.register('story-comments', AdminStoryCommentViewSet, 'story-comment')
router.register('groups', AdminUserGroupViewSet, base_name='group')
router.register('profession-city', AdminProfileCityProfessionSearch,
                base_name='profession_city')
router.register('equipments', AdminEquipmentViewSet, base_name='equipment')
router.register('', AdminUserViewSet, base_name='user')


urlpatterns = [] + router.urls
