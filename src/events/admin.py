from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from events.models import Event, Participation


class EventAdmin(TranslationAdmin):
    pass


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')
    list_filter = ('user', 'event')


admin.site.register(Event, EventAdmin)
admin.site.register(Participation, ParticipationAdmin)
