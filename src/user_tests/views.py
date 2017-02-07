from rest_framework.viewsets import ReadOnlyModelViewSet

from user_tests.models import Test, Task, Question
from user_tests.serializers import TestSerializer, TaskSerializer, QuestionSerializer


class TestViewSet(ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = ()


class TaskViewSet(ReadOnlyModelViewSet):
    queryset = Task.objects.prefetch_related('test').all()
    permission_classes = ()
    serializer_class = TaskSerializer
    filter_fields = ('test',)


class QuestionViewSet(ReadOnlyModelViewSet):
    queryset = Question.objects.prefetch_related('task').all()
    permission_classes = ()
    serializer_class = QuestionSerializer
    filter_fields = ('task', 'task__test',)
