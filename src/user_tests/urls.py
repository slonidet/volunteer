from rest_framework import routers

from user_tests.views import TestViewSet, TaskViewSet, QuestionViewSet


router = routers.DefaultRouter()

router.register('test', TestViewSet, base_name='test')
router.register('tasks', TaskViewSet, base_name='task')
router.register('question', QuestionViewSet, base_name='question')

urlpatterns = [] + router.urls
