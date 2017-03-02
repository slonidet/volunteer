from django.contrib import admin

from notices.models import Notice


class NoticeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Notice, NoticeAdmin)
