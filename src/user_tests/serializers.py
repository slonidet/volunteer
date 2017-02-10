from django.utils import timezone
from rest_framework import serializers

from core.fk_sirializer import ForeignKeySerializerMixin
from user_tests.models import Test, Task, Question, AnswerOptions, UserTest


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        extra_kwargs = {'name': {'validators': []}}


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOptions
        exclude = ('is_correct',)


class UserTestSerializer(ForeignKeySerializerMixin,
                         serializers.ModelSerializer):
    test = TestSerializer()
    remaining = serializers.SerializerMethodField()

    class Meta:
        model = UserTest
        fields = ('id', 'test', 'remaining', 'finished_at',)
        foreign_key_fields = ('test',)

    def get_remaining(self, obj):
        return obj.remaining

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['finished_at'] = timezone.now()

        return super().update(instance, validated_data)
