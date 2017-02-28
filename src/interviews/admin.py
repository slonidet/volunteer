from django.contrib import admin

from interviews.models import Interviewer, Interview


class InterviewerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'interviewer', 'volunteer', 'date', 'period',
                    'status')


admin.site.register(Interviewer, InterviewerAdmin)
admin.site.register(Interview, InterviewAdmin)
