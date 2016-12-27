from django.contrib import admin

from static.models import Page


class PageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Page, PageAdmin)
