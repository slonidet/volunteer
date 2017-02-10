from rest_framework import serializers

from user_tests.models import Test, Task, Question, AnswerOptions, UserTest


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


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


class UserTestSerializer(serializers.ModelSerializer):
    test = TestSerializer()
    remaining = serializers.SerializerMethodField()
    finished = serializers.SerializerMethodField()

    class Meta:
        model = UserTest
        fields = ('id', 'test', 'remaining', 'finished',)

    def get_remaining(self, obj):
        return obj.remaining

    def get_finished(self, obj):
        return obj.finished

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    #
    # def update(self, instance, validated_data):
    #     pass
