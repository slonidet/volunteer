from rest_framework import routers

from user_tests.views import TestViewSet, TaskViewSet, QuestionViewSet, \
    AnswerOptionsViewSet, UserTestViewSet, UserAnswerViewSet

router = routers.DefaultRouter()
router.register('user-tests', UserTestViewSet, base_name='user-test')
router.register('user-answers', UserAnswerViewSet, base_name='user-answer')

router.register('tasks/questions/options', AnswerOptionsViewSet, base_name='option')
router.register('tasks/questions', QuestionViewSet, base_name='question')
router.register('tasks', TaskViewSet, base_name='task')
router.register('', TestViewSet, base_name='test')

urlpatterns = [] + router.urls
