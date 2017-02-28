from django.contrib import admin

from interviews.models import Interviewer, Interview


class InterviewerAdmin(admin.ModelAdmin):
    pass


class InterviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Interviewer, InterviewerAdmin)
admin.site.register(Interview, InterviewAdmin)
