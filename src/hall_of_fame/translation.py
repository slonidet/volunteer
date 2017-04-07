from modeltranslation.translator import translator, TranslationOptions

from hall_of_fame.models import HallOfFame


class NHallOfFameTranslationOptions(TranslationOptions):
    fields = ('text', )
    required_languages = ('ru', 'en',)


translator.register(HallOfFame, NHallOfFameTranslationOptions)
