from rest_framework import mixins
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from user_tests.models import Test, Task, Question, AnswerOptions, UserTest
from user_tests.serializers import TestSerializer, TaskSerializer, \
    QuestionSerializer, AnswerOptionsSerializer, UserTestSerializer


class TestViewSet(ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    permission_classes = ()
    serializer_class = TestSerializer


class TaskViewSet(ReadOnlyModelViewSet):
    queryset = Task.objects.prefetch_related('test').all()
    permission_classes = ()
    serializer_class = TaskSerializer
    filter_fields = ('test',)


class QuestionViewSet(ReadOnlyModelViewSet):
    queryset = Question.objects.prefetch_related('task').all()
    permission_classes = ()
    serializer_class = QuestionSerializer
    filter_fields = ('task__test', 'task',)


class AnswerOptionsViewSet(ReadOnlyModelViewSet):
    queryset = AnswerOptions.objects.all()
    permission_classes = ()
    serializer_class = AnswerOptionsSerializer
    filter_fields = ('question__task', 'question',)


class UserTestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      GenericViewSet):
    queryset = UserTest.objects.select_related('user')
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserTestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)
