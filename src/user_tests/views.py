from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.views import UndeletableModelViewSet
from user_tests.models import Test, Task, Question, AnswerOptions, UserTest, \
    UserAnswer
from user_tests.serializers import TestSerializer, TaskSerializer, \
    QuestionSerializer, AnswerOptionsSerializer, UserTestSerializer, \
    UserAnswerSerializer, AdminUserTestSerializer, \
    AdminAverageTestScoreSerializer
from users.models import User


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

    def create(self, request, *args, **kwargs):
        if request.user.role not in (User.ROLE_APPROVED, User.ROLE_TESTED):
            raise exceptions.NotAcceptable(
                _('Проходить тесты можно только после утверждения анкеты '
                  'администратором')
            )

        return super().create(request, *args, **kwargs)


class UserAnswerViewSet(BaseUserTestViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    filter_fields = ('question', 'question__task__test__name')


class AdminUserTestViewSet(ReadOnlyModelViewSet):
    queryset = UserTest.objects.select_related('test', 'user').filter(
        finished_at__isnull=False)
    serializer_class = AdminUserTestSerializer
    filter_fields = ('test', 'user')

    def list(self, request, *args, **kwargs):
        if 'user' not in request.query_params:
            raise exceptions.NotAcceptable(
                _('Данный метод доступен только с фильтрацией по user')
            )

        return super().list(request, *args, **kwargs)


class AdminAverageTestScore(ReadOnlyModelViewSet):
    queryset = Test.objects.prefetch_related('tasks').all()
    serializer_class = AdminAverageTestScoreSerializer
    filter_fields = ('name', 'type')
