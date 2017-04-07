from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from hall_of_fame.models import HallOfFame


class HallOfFameModelAdmin(TranslationAdmin):
    pass


admin.site.register(HallOfFame, HallOfFameModelAdmin)
