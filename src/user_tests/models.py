from functools import lru_cache

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField

from permissions.models import MetaPermissions
from users.models import User, Profile


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

    @classmethod
    @lru_cache()
    def get_factor_list(cls):
        return dict(cls.FACTOR_CHOICES).keys()


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
        max_choices=2, max_length=8
    )

    class Meta(MetaPermissions):
        verbose_name = _('Вариант ответа Каттелла')
        verbose_name_plural = _('Варианты ответов Каттелла')

    def __str__(self):
        return str(self.id)

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

    class Meta(MetaPermissions):
        verbose_name = _('Стен Каттелла')
        verbose_name_plural = _('Стены Каттелла')

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_sten(cls, factor, score):
        return cls.objects.get(factor=factor, score=score).sten

    @classmethod
    def factor_polarization(cls, factor, score, user):
        sten = cls.get_sten(factor, score)
        factor_borders = {
            cls.FACTOR_A: 6,
            cls.FACTOR_B: 3,
            cls.FACTOR_C: 6,
            cls.FACTOR_E: 5,
            cls.FACTOR_F: 5,
            cls.FACTOR_G: 6,
            cls.FACTOR_H: 5,
            cls.FACTOR_L: 5,
            cls.FACTOR_M: 5,
            cls.FACTOR_N: 5,
            cls.FACTOR_O: 6,
            cls.FACTOR_Q1: 6,
            cls.FACTOR_Q2: 5,
            cls.FACTOR_Q3: 5,
            cls.FACTOR_Q4: 7,
        }

        if factor == cls.FACTOR_MD:
            if sten <= 4:
                polarization = '{0}-'
            elif 4 < sten < 10:
                polarization = '{0}'
            else:
                polarization = '{0}+'

        elif factor == cls.FACTOR_I:
            border = 5 if user.profile.gender == Profile.GENDER_MALE else 6
            polarization = '{0}-' if sten <= border else '{0}+'
        else:
            border = factor_borders.get(factor)
            polarization = '{0}-' if sten <= border else '{0}+'

        return polarization.format(factor)


CattellInterpretation = {
    'Социально-психологические особенности: экстраверсия - интроверсия': (
        ({'A-', 'F-', 'H-'}, 'Сдержанность в межличностных контактах, трудности в непосредственном и социальном общении, склонность к индивидуальной работе, замкнутость, направленность на свой внутренний мир. Интроверсия.'),
        ({'A-', 'F+', 'H-'}, 'Сдержанность в установлении как межличностных, так и социальных контактов. В поведении - экспрессивность, импульсивность, в характере проявляются застенчивость и внешняя активность, склонность к индивидуальной деятельности Склонность к интроверсии.'),
        ({'A+', 'F-', 'H-'}, 'Открытость в межличностных контактах, способность к непосредственному общению, сдержанность и рассудительность в установлении социальных контактов, осторожность и застенчивость.'),
        ({'A+', 'F-', 'H+'}, 'Открытость в межличностных контактах, активность, общительность, готовность к вступлению в новые группы, сдержанность и рассудительность в выборе партнеров по общению. Склонность к экстраверсии.'),
        ({'A-', 'F+', 'H+'}, 'Сдержанность в непосредственных межличностных контактах, активность, экспрессивность в социальном общении, готовность к вступлению в новые группы, склонность к лидерству. Склонность к экстраверсии.'),
        ({'A-', 'F-', 'H+'}, 'Сдержанность и рассудительность в установлении межличностных контактов, активность в социальной сфере, может проявляться деловое лидерство.'),
        ({'A+', 'F+', 'H-'}, 'Открытость, экспрессивность, импульсивность в межличностном общении. Трудность в установлении социальных контактов, проявление застенчивости в новых, незнакомых обстоятельствах, затруднения при принятии социальных решений.'),
        ({'A+', 'F+', 'H+'}, 'Открытость, общительность, активность в установлении как межличностных, так и социальных контактов. В поведении проявляются экспрессивность, импульсивность, социальная смелость, склонность к риску, готовность к вступлению в новые группы, быть лидером. Направленность вовне, на людей. Экстраверсия.'),
    ),
    'Социально-психологические особенности: коммуникативные свойства': (
        ({'Е+', 'Q2+', 'G+', 'N+', 'L+'}, 'Независимость характера, склонность к доминантности, авторитарности, настороженность по отношению к людям, противопоставление себя группе, склонность к лидерству, развитое чувство ответственности и долга, принятие правил и норм, самостоятельность в принятии решений, инициативность, активность в социальных сферах, гибкость и дипломатичность в межличностном общении, умение находить нетривиальные решения в практических, житейских ситуациях.'),
    )
}


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
    is_limited = models.BooleanField(
        _('Ограничение времени прохождения теста'), default=True
    )

    class Meta(MetaPermissions):
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Test's task
    """
    ALGORITHM_AUTO_APPRAISAL = 'auto_appraisal'
    ALGORITHM_EXPERT_APPRAISAL = 'expert_appraisal'
    ALGORITHM_PSYCHOLOGICAL = 'psychological'
    ALGORITHM_CHOICES = (
        (ALGORITHM_AUTO_APPRAISAL, _('Проверяется автоматически')),
        (ALGORITHM_EXPERT_APPRAISAL, _('Проверяется экспертом')),
        (ALGORITHM_PSYCHOLOGICAL, _('Задание психологического теста'))
    )

    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, verbose_name=_('Тест'),
        related_name='tasks'
    )
    name = models.CharField(_('Название задания'), max_length=150)
    evaluation_algorithm = models.CharField(
        _('Алгоритм проверки'), max_length=50,
        choices=ALGORITHM_CHOICES, default=ALGORITHM_AUTO_APPRAISAL
    )
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
    number = models.IntegerField(
        _('Номер вопроса'), null=True, blank=True
    )
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
    number = models.CharField(
        _('Номер ответа'), choices=CattellOptions.ANSWER_CHOICES,
        null=True, blank=True, max_length=1
    )
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
