from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.views import UndeletableModelViewSet
from user_tests.models import Test, Task, Question, AnswerOptions, UserTest, \
    UserAnswer
from user_tests.serializers import TestSerializer, TaskSerializer, \
    QuestionSerializer, AnswerOptionsSerializer, UserTestSerializer, \
    UserAnswerSerializer, AdminUserTestSerializer


class BaseTestReadOnlyModelViewSet(ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None


class TestViewSet(BaseTestReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TaskViewSet(BaseTestReadOnlyModelViewSet):
    queryset = Task.objects.prefetch_related('test').all()
    serializer_class = TaskSerializer
    filter_fields = ('test', 'test__name')


class QuestionViewSet(BaseTestReadOnlyModelViewSet):
    queryset = Question.objects.select_related('task')
    serializer_class = QuestionSerializer
    filter_fields = ('task', 'task__test', 'task__test__name')


class AnswerOptionsViewSet(BaseTestReadOnlyModelViewSet):
    queryset = AnswerOptions.objects.all()
    serializer_class = AnswerOptionsSerializer
    filter_fields = ('question', 'question__task__test__name')


class BaseUserTestViewSet(UndeletableModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)


class UserTestViewSet(BaseUserTestViewSet):
    queryset = UserTest.objects.all()
    serializer_class = UserTestSerializer


class UserAnswerViewSet(BaseUserTestViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    filter_fields = ('question', 'question__task__test__name')


class AdminUserTestViewSet(ReadOnlyModelViewSet):
    queryset = UserTest.objects.select_related('test').all()
    serializer_class = AdminUserTestSerializer
