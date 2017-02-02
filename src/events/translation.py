from modeltranslation.translator import translator, TranslationOptions

from events.models import Event


class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address', )
    required_languages = ('ru', 'en',)


translator.register(Event, EventTranslationOptions)
