from modeltranslation.translator import translator, TranslationOptions
from news.models import News


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)
    required_languages = ('ru', 'en',)


translator.register(News, NewsTranslationOptions)
