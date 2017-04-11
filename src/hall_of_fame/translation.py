from modeltranslation.translator import translator, TranslationOptions

from hall_of_fame.models import HallOfFame


class HallOfFameTranslationOptions(TranslationOptions):
    fields = ('text', )
    required_languages = ('ru', 'en',)


translator.register(HallOfFame, HallOfFameTranslationOptions)
