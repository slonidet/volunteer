from core.translation_serializers import AdminTranslationModelSerializer, \
    UserTranslationModelSerializer
from static.models import Page
from static.translation import PageTranslationOptions


class AdminPageSerializer(AdminTranslationModelSerializer):
    class Meta:
        model = Page
        model_translation = PageTranslationOptions
        fields = '__all__'
        lookup_field = 'slug'


class PageSerializer(UserTranslationModelSerializer):
    class Meta(AdminPageSerializer.Meta):
        pass
