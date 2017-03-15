from django.contrib import admin

from user_tests.models import Test, UserTest, Task, Question, AnswerOptions, \
    CattellSten, CattellOptions


class QuestionInline(admin.TabularInline):
    model = Question


class TaskInline(admin.TabularInline):
    model = Task


class AnswerOptionsInline(admin.TabularInline):
    model = AnswerOptions


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'time_available')
    list_filter = ('type',)
    inlines = [TaskInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'test', 'evaluation_algorithm')
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'task')
    list_filter = ('task__test',)
    inlines = [AnswerOptionsInline]


class AnswerOptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_correct', 'question')
    list_filter = ('question__task__test',)


class CattellStenAdmin(admin.ModelAdmin):
    list_display = ('sten', 'factor', 'score')


class CattellOptionsAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'factor')


class UserTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test', 'started_at', 'finished_at')
    list_filter = ('test',)
    search_fields = ('user__username', 'user__profile__first_name',
                     'user__profile__last_name', 'user__profile__middle_name')


admin.site.register(Test, TestAdmin)
admin.site.register(UserTest, UserTestAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOptions, AnswerOptionsAdmin)
admin.site.register(CattellSten, CattellStenAdmin)
admin.site.register(CattellOptions, CattellOptionsAdmin)
