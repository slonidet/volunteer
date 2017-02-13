from rest_framework import permissions

from core.views import UndeletableModelViewSet, ListArrayViewSet
from user_tests.models import Test, Task, Question, AnswerOptions, UserTest, \
    UserAnswer
from user_tests.serializers import TestSerializer, TaskSerializer, \
    QuestionSerializer, AnswerOptionsSerializer, UserTestSerializer, \
    UserAnswerSerializer


class TestViewSet(ListArrayViewSet):
    queryset = Test.objects.all()
    permission_classes = ()
    serializer_class = TestSerializer


class TaskViewSet(ListArrayViewSet):
    queryset = Task.objects.prefetch_related('test').all()
    permission_classes = ()
    serializer_class = TaskSerializer
    filter_fields = ('test',)


class QuestionViewSet(ListArrayViewSet):
    queryset = Question.objects.prefetch_related('task').all()
    permission_classes = ()
    serializer_class = QuestionSerializer
    filter_fields = ('task__test', 'task',)


class AnswerOptionsViewSet(ListArrayViewSet):
    queryset = AnswerOptions.objects.all()
    permission_classes = ()
    serializer_class = AnswerOptionsSerializer
    filter_fields = ('question__task', 'question',)


class BaseUserViewSet(UndeletableModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)


class UserTestViewSet(BaseUserViewSet):
    queryset = UserTest.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserTestSerializer


class UserAnswerViewSet(BaseUserViewSet):
    queryset = UserAnswer.objects.prefetch_related('answer_values')
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserAnswerSerializer
