from rest_framework.viewsets import ReadOnlyModelViewSet

from user_tests.models import Test, Task, Question, AnswerOptions
from user_tests.serializers import TestSerializer, TaskSerializer, \
    QuestionSerializer, AnswerOptionsSerializer


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
