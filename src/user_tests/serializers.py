from django.db import IntegrityError
from django.db.models import Count
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
        user_test = UserTest.objects.filter(
            user=user, test=question.task.test).first()
        time_expired_message = _('Время отведённое на тест истекло')

        if not user_test:
            message = _('Нужно начать тест, прежде чем давать ответы на него')
            raise ValidationError(message)

        elif not user_test.finished_at and user_test.remaining <= 0:
            user_test.finished_at = timezone.now()
            user_test.save()
            raise ValidationError(time_expired_message)

        elif user_test.finished_at:
            raise ValidationError(time_expired_message)

    def _check_correct_answers(self, validated_data):
        expert_appraisal = validated_data['question'].task.expert_appraisal
        if not expert_appraisal:
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


class AdminTaskSerializer(TaskSerializer):
    formatted_answers = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()

    def get_questions_count(self, obj):
        return Question.objects.filter(task=obj).count()

    def get_formatted_answers(self, obj):
        answers = UserAnswer.objects.filter(user=)
        questions = obj.questions.prefetch_related('answers').filter()
        answers = [
            {
                'question_text': q.text,
                'user_answers': q.user_answers.answers,
                'is_correct': q.
            } for q in questions
        ]
        return Question.objects.filter(task=obj).count()

    class Meta(TaskSerializer.Meta):
        fields = (
            'id', 'name', 'evaluation_algorithm', 'questions_count',
            'formatted_answers',
        )


class AdminTestSerializer(TestSerializer):
    tasks = AdminTaskSerializer(many=True, read_only=True)

    class Meta(TestSerializer.Meta):
        fields = ('id', 'name', 'tasks')


class AdminUserTestSerializer(UserTestSerializer):
    test = AdminTestSerializer(read_only=True)

    class Meta(UserTestSerializer.Meta):
        model = UserTest
        fields = ['id', 'user', 'test', 'finished_at', 'started_at']
