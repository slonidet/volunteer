from django.core.cache import cache
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from core.serializers import ForeignKeySerializerMixin
from user_tests.models import Test, Task, Question, AnswerOptions, UserTest, \
    UserAnswer, CattellOptions, CattellFactorMixin, CattellSten, \
    CattellInterpretation


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        extra_kwargs = {'name': {'validators': []}}


class SimpleTestSerializer(TestSerializer):
    class Meta(TestSerializer.Meta):
        fields = ('id', 'name', 'is_limited')


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
        test = instance.test

        if test.type == Test.TYPE_PSYCHOLOGICAL:
            test_questions = Question.objects.filter(task__test=test)
            user_answers = UserAnswer.objects.filter(
                question__in=test_questions
            )
            if user_answers.count() < test_questions.count():
                raise serializers.ErrorDetail(
                    _('Пользователь ответил не на все вопросы')
                )

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
            if test.is_limited:
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
            'psychological_characteristic': self._psychological_characteristic(
                task, user
            )
        }

    def _psychological_characteristic(self, task, user):
        if task.evaluation_algorithm != Task.ALGORITHM_PSYCHOLOGICAL:
            return None

        user_cache_key = 'psychological_characteristic_{0}'.format(user.id)
        result = cache.get(user_cache_key)
        if result:
            return result

        factors = CattellFactorMixin.get_factor_list()
        try:
            factor_scores = {
                factor: self.__get_factor_scores(task, factor, user)
                for factor in factors
            }
        except ValueError as e:
            return str(e)

        polarized_factors = set()
        for factor, score in factor_scores.items():
            polarized = CattellSten.factor_polarization(factor, score, user)
            polarized_factors.add(polarized)

        result = {}
        for parameter, characteristics in CattellInterpretation.items():
            for factor_set, description in characteristics:
                if factor_set.issubset(polarized_factors):
                    result[parameter] = description
                    break

        # cache user psychological characteristic
        cache.set(user_cache_key, result, 60*60*24*30)

        return result

    @staticmethod
    def __get_factor_scores(task, factor, user):
        raw_scores = 0
        question_numbers = CattellOptions.objects.filter(factor=factor).\
            values_list('question_number', flat=True)
        user_answers = UserAnswer.objects.select_related('question').filter(
            user=user, question__task=task,
            question__number__in=question_numbers,
        )

        if question_numbers.count() != user_answers.count():
            # if user didn't answer to question pass it instead crash
            raise ValueError('user did not answer on all questions')

        for answer in user_answers:
            try:
                answer_option = AnswerOptions.objects.get(
                    question=answer.question, text=','.join(answer.answers)
                )
            except AnswerOptions.DoesNotExist:
                # Unreal achtung! Select first answer if user answer not fount
                # because frontend sent wrong answer text
                answer_option = AnswerOptions.objects.filter(
                    question=answer.question).first()

            raw_scores += CattellOptions.objects.get(
                factor=factor, question_number=answer.question.number
            ).get_score(choice=answer_option.number)

        return raw_scores

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

