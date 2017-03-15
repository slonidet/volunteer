from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField

from permissions.models import MetaPermissions
from users.models import User


class Test(models.Model):
    """
    Test model
    """
    TYPE_VERBAL = 'verbal'
    TYPE_NUMERICAL = 'numerical'
    TYPE_PSYCHOLOGICAL = 'psychological'
    TYPE_FOREIGN_LANGUAGE = 'foreign'
    TYPE_CHOICES = (
        (TYPE_VERBAL, _('Вербальный')),
        (TYPE_NUMERICAL, _('Числовой')),
        (TYPE_PSYCHOLOGICAL, _('Психологический')),
        (TYPE_FOREIGN_LANGUAGE, _('Иностранный язык')),
    )
    name = models.CharField(_('Название'), max_length=150, unique=True)
    type = models.CharField(_('Тип'), max_length=16, choices=TYPE_CHOICES)
    time_available = models.IntegerField(_('Доступное время в секундах'))

    class Meta(MetaPermissions):
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Test's task
    """
    AUTO_APPRAISAL = 'auto_appraisal'
    EXPERT_APPRAISAL = 'expert_appraisal'
    PSYCHOLOGICAL = 'psychological'
    ALGORITHM_CHOICES = (
        (AUTO_APPRAISAL, _('Проверяется автоматически')),
        (EXPERT_APPRAISAL, _('Проверяется экспертом')),
        (PSYCHOLOGICAL, _('Задание психологического теста'))
    )

    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, verbose_name=_('Тест'),
        related_name='tasks'
    )
    name = models.CharField(_('Название задания'), max_length=150)
    evaluation_algorithm = models.CharField(
        _('Алгоритм проверки'),
        max_length=50,
        choices=ALGORITHM_CHOICES,
        default=AUTO_APPRAISAL
    )
    audio = models.FileField(_('Аудиофайл'), null=True, blank=True)
    text = models.TextField(_('Текст'), null=True, blank=True)

    class Meta(MetaPermissions):
        verbose_name = _('Задание')
        verbose_name_plural = _('Задания')

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Question model
    """
    text = models.CharField(_('Текст вопроса'), max_length=250)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name=_('Задание'),
        related_name='questions'
    )

    class Meta(MetaPermissions):
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__(self):
        return self.text


class AnswerOptions(models.Model):
    """
    Options of given answer
    """
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_('Вопрос'),
        related_name='answer_options'
    )
    text = models.CharField(_('Текст ответа'), max_length=250)
    is_correct = models.NullBooleanField(_('Правильность ответа'), null=True)

    class Meta(MetaPermissions):
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответа')

    def __str__(self):
        return self.text


class UserTest(models.Model):
    """
    Test of given user
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Пользователь'),
        related_name='tests'
    )
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, verbose_name=_('Тест')
    )
    started_at = models.DateTimeField(
        _('Время начала тестирования'), auto_now_add=True
    )
    finished_at = models.DateTimeField(_('Время окончания тестирования'),
                                       null=True, blank=True)

    class Meta(MetaPermissions):
        verbose_name = _('Тест пользователя')
        verbose_name_plural = _('Тесты пользователя')
        unique_together = ('user', 'test')

    def __str__(self):
        return str(self.id)

    @property
    def remaining(self):
        dead_line = self.started_at + timezone.timedelta(
            seconds=self.test.time_available
        )
        remaining = dead_line - timezone.now()
        remaining = int(remaining.total_seconds())
        is_not_finished = remaining > 0 and not self.finished_at
        remaining = remaining if is_not_finished else 0

        return remaining


class UserAnswer(models.Model):
    """
    Answers of given user
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Пользователь')
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_('Вопрос'),
        related_name='user_answers')
    answers = MultiSelectField(_('Ответы пользователя'), max_length=8192)
    is_correct = models.NullBooleanField(_('Правльность ответов'), null=True)

    class Meta(MetaPermissions):
        verbose_name = _('Ответы пользователя')
        verbose_name_plural = _('Ответы пользователей')
        unique_together = ('user', 'question')

    def __str__(self):
        return str(self.id)


class CattellFactorMixin(object):
    """
    Cattell factors
    """
    FACTOR_A = 'A'
    FACTOR_B = 'B'
    FACTOR_C = 'C'
    FACTOR_E = 'E'
    FACTOR_F = 'F'
    FACTOR_G = 'G'
    FACTOR_H = 'H'
    FACTOR_I = 'I'
    FACTOR_L = 'L'
    FACTOR_M = 'M'
    FACTOR_N = 'N'
    FACTOR_O = 'O'
    FACTOR_Q1 = 'Q1'
    FACTOR_Q2 = 'Q2'
    FACTOR_Q3 = 'Q3'
    FACTOR_Q4 = 'Q4'
    FACTOR_MD = 'MD'
    FACTOR_CHOICES = (
        (FACTOR_A, 'A'), (FACTOR_B, 'B'), (FACTOR_C, 'C'), (FACTOR_E, 'E'),
        (FACTOR_F, 'F'), (FACTOR_G, 'G'), (FACTOR_H, 'H'), (FACTOR_I, 'I'),
        (FACTOR_L, 'L'), (FACTOR_M, 'M'), (FACTOR_N, 'N'), (FACTOR_O, 'O'),
        (FACTOR_Q1, 'Q1'), (FACTOR_Q2, 'Q2'), (FACTOR_Q3, 'Q3'),
        (FACTOR_Q4, 'Q4'), (FACTOR_MD, 'MD'),
    )


class CattellOptions(CattellFactorMixin, models.Model):
    """
    Options for psychological test
    """
    ANSWER_A = 'a'
    ANSWER_B = 'b'
    ANSWER_C = 'c'
    ANSWER_CHOICES = ((ANSWER_A, 'a'), (ANSWER_B, 'b'), (ANSWER_C, 'c'))

    question_number = models.IntegerField(_('Номер вопроса'))
    factor = models.CharField(
        _('Психологический фактор'), max_length=2,
        choices=CattellFactorMixin.FACTOR_CHOICES
    )
    answer_options = MultiSelectField(
        _('Варианты ответа в ключе'), choices=ANSWER_CHOICES,
        max_choices=2, max_length=1
    )

    def get_score(self, choice):
        if choice in self.answer_options:
            if self.factor == 'B':
                return 1
            if choice in 'ac':
                return 2
            if choice in 'b':
                return 1

        return 0


class CattellSten(CattellFactorMixin, models.Model):
    """
    Final score (stens)
    """
    sten = models.IntegerField(_('Количество стенов'))
    factor = models.CharField(
        _('Психологический фактор'), max_length=2,
        choices=CattellFactorMixin.FACTOR_CHOICES
    )
    score = models.IntegerField(_('Количество сырых баллов'))

    @classmethod
    def get_sten(cls, factor, score):
        return cls.objects.get(factor=factor, score=score).sten
