from modeltranslation.translator import translator, TranslationOptions

from users.models import Story


class StoryTranslationOptions(TranslationOptions):
    fields = ('text', 'about_yourself',)


translator.register(Story, StoryTranslationOptions)
