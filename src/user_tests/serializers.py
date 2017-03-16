from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from core.serializers import ForeignKeySerializerMixin
from user_tests.models import Test, Task, Question, AnswerOptions, UserTest, \
    UserAnswer


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        extra_kwargs = {'name': {'validators': []}}


class SimpleTestSerializer(TestSerializer):
    class Meta(TestSerializer.Meta):
        fields = ('id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class AnswerOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOptions
        exclude = ('is_correct',)


class SimpleAnswerOptionsSerializer(AnswerOptionsSerializer):
    class Meta(AnswerOptionsSerializer.Meta):
        exclude = ('is_correct', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class BaseUserTestSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)


class UserTestSerializer(ForeignKeySerializerMixin,
                         BaseUserTestSerializer):
    test = SimpleTestSerializer()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = UserTest
        fields = ('id', 'test', 'remaining', 'finished_at',)
        foreign_key_fields = ('test',)

    def get_remaining(self, obj):
        return obj.remaining

    def create(self, validated_data):
        user = self.context['request'].user
        test_already_exist = UserTest.objects.filter(
            user=user, test__name=validated_data['test']['name']).exists()

        if test_already_exist:
            message = _('Пользователь уже проходил этот тест')
            raise ValidationError(message, code='unique')

        try:
            # you cannot finish the test when creating
            validated_data.pop('finished_at')
        except KeyError:
            pass

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['finished_at'] = timezone.now()

        return super().update(instance, validated_data)


class UserAnswerSerializer(BaseUserTestSerializer):
    answers = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        label=UserAnswer._meta.get_field('answers').verbose_name,
    )

    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'answers']

    def validate(self, data):
        user = self.context['request'].user
        question = data['question']
        self._check_available_test(question, user)

        return data

    @staticmethod
    def _check_available_test(question, user):
        """ User's Test is available for passing """
        test = question.task.test
        user_test = UserTest.objects.filter(user=user, test=test).first()
        time_expired_message = _('Время отведённое на тест истекло')

        if not user_test:
            message = _('Нужно начать тест, прежде чем давать ответы на него')
            raise ValidationError(message)

        elif not user_test.finished_at and user_test.remaining <= 0:
            if test.type != test.TYPE_PSYCHOLOGICAL:
                # PSYCHOLOGICAL test is unlimited
                user_test.finished_at = timezone.now()
                user_test.save()
                raise ValidationError(time_expired_message)

        elif user_test.finished_at:
            raise ValidationError(time_expired_message)

    def _check_correct_answers(self, validated_data):
        algorithm = validated_data['question'].task.evaluation_algorithm
        if algorithm == Task.ALGORITHM_AUTO_APPRAISAL:
            user_answers = set(validated_data['answers'])
            correct_answers = set(AnswerOptions.objects.filter(
                question=validated_data['question'],
                is_correct=True
            ).values_list('text', flat=True))

            validated_data['is_correct'] = (user_answers == correct_answers)

        return validated_data

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        error_message = _('Пользователь уже отвечал на этот вопрос')

        user_answer = UserAnswer.objects.filter(user=user, question=question)
        if user_answer.exists():
            raise ValidationError(error_message, code='unique')

        validated_data = self._check_correct_answers(validated_data)

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(error_message, code='unique')

    def update(self, instance, validated_data):
        validated_data = self._check_correct_answers(validated_data)
        return super().update(instance, validated_data)


class AdminUserTestSerializer(UserTestSerializer):
    test = TestSerializer(read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta(UserTestSerializer.Meta):
        model = UserTest
        fields = ['id', 'user', 'test', 'tasks', 'finished_at', 'started_at']

    def get_tasks(self, user_test):
        user = user_test.user
        user_tasks = user_test.test.tasks.all()

        return [self._task_repr(task, user) for task in user_tasks]

    def _task_repr(self, task, user):
        return {
            'id': task.id,
            'name': task.name,
            'evaluation_algorithm': task.evaluation_algorithm,
            'questions_count': task.questions.count(),
            'correct_answers_count': UserAnswer.objects.filter(
                user=user, question__in=task.questions.all(),
                is_correct=True
            ).count(),
            'formatted_answers': self._user_answers_repr(
                task, user
            ),
        }

    def _user_answers_repr(self, task, user):
        user_answers = UserAnswer.objects.select_related('question').filter(
            user=user, question__in=task.questions.all()
        )
        return [
            {
                'question_text': a.question.text,
                'user_answers': a.answers,
                'is_correct': a.is_correct,
            } for a in user_answers
        ]


class AdminAverageTaskScoreSerializer(TaskSerializer):
    average_score = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()

    class Meta(TaskSerializer.Meta):
        fields = ('name', 'evaluation_algorithm', 'average_score',
                  'questions_count')

    def get_average_score(self, task):
        if task.evaluation_algorithm == Task.ALGORITHM_AUTO_APPRAISAL:
            total_correct_answers = UserAnswer.objects.filter(
                question__task=task, is_correct=True
            ).count()
            users_passed_test = UserTest.objects.filter(test=task.test).count()

            if users_passed_test > 0:
                return round(total_correct_answers / users_passed_test, 2)

        return None

    def get_questions_count(self, task):
        return task.questions.count()


class AdminAverageTestScoreSerializer(serializers.ModelSerializer):
    tasks = AdminAverageTaskScoreSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = '__all__'

