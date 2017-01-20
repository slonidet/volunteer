from modeltranslation.translator import translator, TranslationOptions

from users.models import Story


class StoryTranslationOptions(TranslationOptions):
    fields = ('text', 'about_yourself',)
    required_languages = ('ru', 'en',)


translator.register(Story, StoryTranslationOptions)
