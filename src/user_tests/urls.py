from rest_framework import routers

from user_tests.views import TestViewSet, TaskViewSet, QuestionViewSet, \
    AnswerOptionsViewSet


router = routers.DefaultRouter()

router.register('tasks', TaskViewSet, base_name='task')
router.register('questions', QuestionViewSet, base_name='question')
router.register('options', AnswerOptionsViewSet, base_name='option')
router.register('', TestViewSet, base_name='test')

urlpatterns = [] + router.urls
