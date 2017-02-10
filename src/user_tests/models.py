from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from permissions.models import MetaPermissions
from users.models import User


class Test(models.Model):
    """
    Test model
    """
    name = models.CharField(_('Название теста'), max_length=150, unique=True)
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
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, verbose_name=_('Тест')
    )
    name = models.CharField(_('Название задания'), max_length=150)
    expert_appraisal = models.BooleanField(_('Проверяется администратором'))
    audio = models.FileField(_('Аудиофайл'), null=True)
    text = models.TextField(_('Текст'), null=True)

    class Meta(MetaPermissions):
        verbose_name = _('Задание')
        verbose_name_plural = _('Задания')

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Question model
    """
    text = models.CharField(_('Текст вопроса'), max_length=150)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name=_('Задание')
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
        Question, on_delete=models.CASCADE, verbose_name=_('Вопрос')
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
        User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, verbose_name=_('Тест')
    )
    started_at = models.DateTimeField(
        _('Время начала тестирования'), auto_now_add=True
    )
    finished_at = models.DateTimeField(_('Время окончания тестирования'),
                                       null=True, blank=True)

    @property
    def remaining(self):
        dead_line = self.started_at + timezone.timedelta(
            seconds=self.test.time_available
        )
        remaining = dead_line - timezone.now()
        remaining = int(remaining.total_seconds())
        remaining = remaining if remaining > 0 else 0

        return remaining

    @property
    def finished(self):
        return True if self.remaining >= 0 else False

    class Meta(MetaPermissions):
        verbose_name = _('Тест пользователя')
        verbose_name_plural = _('Тесты пользователя')

    def __str__(self):
        return self.id


class UserAnswer(models.Model):
    """
    Answers of given user
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('Пользователь')
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_('Вопрос')
    )
    is_correct = models.NullBooleanField(_('Правльность ответов'), null=True)

    class Meta(MetaPermissions):
        verbose_name = _('Ответы пользователя')
        verbose_name_plural = _('Ответы пользователей')

    def __str__(self):
        return self.id


class UserAnswerValue(models.Model):
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE,
                                    verbose_name=_('Ответы пользователя'))
    answers_values = models.TextField(_('Значение ответа пользователя'))

    class Meta(MetaPermissions):
        verbose_name = _('Значение ответа')
        verbose_name_plural =_('Значения ответов пользователя')

    def __str__(self):
        return self.id
