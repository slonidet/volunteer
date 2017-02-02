from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from events.models import Event


class EventAdmin(TranslationAdmin):
    pass

admin.site.register(Event, EventAdmin)
