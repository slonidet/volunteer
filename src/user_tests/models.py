from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User


class Test(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Название теста'))
    time_available = models.IntegerField(verbose_name=_('Доступное время'))

    class Meta():
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')

    def __str__(self):
        return self.name


class Task(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name=_('Тест'))
    name = models.CharField(max_length=150, verbose_name=_('Название задания'))
    questions_number = models.IntegerField(verbose_name=_('Количество вопросов'))
    expert_appraisal = models.BooleanField(verbose_name=_('Проверяется администратором'))

    class Meta():
        verbose_name = _('Задание')
        verbose_name_plural = _('Задания')

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Текст вопроса'))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('Задание'))

    class Meta():
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__(self):
        return self.name


class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name=_('Тест'))
    started_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Время начала тестирования'))
    finished_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Время окончания тестирования'))

    class Meta():
        verbose_name = _('Тест пользователя')
        verbose_name_plural = _('Тесты пользователя')

    def __str__(self):
        return self.id


class AnswerOptions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('Вопрос'))
    name = models.CharField(max_length=250, verbose_name=_('Текст ответа'))
    is_correct = models.BooleanField(verbose_name=_('Правильность ответа'))

    class Meta():
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответа')

    def __str__(self):
        return self.name


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    answers = models.ManyToManyField(AnswerOptions, verbose_name=_('Ответы'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('Вопрос'))
    is_correct = models.NullBooleanField(null=True, verbose_name=_('Правльность ответов'))

    class Meta():
        verbose_name = _('Ответы пользователя')
        verbose_name_plural = _('Ответы пользователей')

    def __str__(self):
        return self.id
