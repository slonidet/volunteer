from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from static.models import Page


class PageAdmin(TranslationAdmin):
    pass


admin.site.register(Page, PageAdmin)
