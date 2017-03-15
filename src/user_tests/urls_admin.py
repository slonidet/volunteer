from rest_framework import routers

from user_tests.views import AdminUserTestViewSet, AdminAverageTestScore

router = routers.DefaultRouter()
router.register('average-scores', AdminAverageTestScore,
                base_name='average-score')
router.register('', AdminUserTestViewSet, base_name='user-answer')


urlpatterns = [] + router.urls
