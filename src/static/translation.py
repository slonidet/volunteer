from modeltranslation.translator import translator, TranslationOptions

from static.models import Page


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)
    required_languages = ('ru', 'en',)


translator.register(Page, PageTranslationOptions)
