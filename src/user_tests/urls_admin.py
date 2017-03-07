from rest_framework import routers

from user_tests.views import AdminUserAnswerViewSet


router = routers.DefaultRouter()
router.register('', AdminUserAnswerViewSet, base_name='user-answer')


urlpatterns = [] + router.urls
