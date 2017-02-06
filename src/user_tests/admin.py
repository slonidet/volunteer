from django.contrib import admin

from user_tests.models import Test, UserTest, Task, Question, AnswerOptions


class QuestionInline(admin.TabularInline):
    model = Question


class TaskInline(admin.TabularInline):
    model = Task


class AnswerOptionsInline(admin.TabularInline):
    model = AnswerOptions


class TestAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
    ]


class UserTestAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerOptionsInline,
    ]


class AnswerOptionsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Test, TestAdmin)
admin.site.register(UserTest, UserTestAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOptions, AnswerOptionsAdmin)
