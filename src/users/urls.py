from rest_framework import routers

from users.views import StoryViewSet


router = routers.DefaultRouter()
router.register('stories', StoryViewSet, base_name='story')


urlpatterns = [] + router.urls
