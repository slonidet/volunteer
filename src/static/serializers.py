from rest_framework.validators import UniqueValidator

from core.fields import SlugField
from core.translation_serializers import AdminTranslationModelSerializer, \
    UserTranslationModelSerializer
from static.models import Page
from static.translation import PageTranslationOptions


class AdminPageSerializer(AdminTranslationModelSerializer):
    slug = SlugField(label='Заголовок в URL', max_length=50,
                     validators=[UniqueValidator(
                         queryset=Page.objects.all())])

    class Meta:
        model = Page
        model_translation = PageTranslationOptions
        fields = '__all__'
        lookup_field = 'slug'


class PageSerializer(UserTranslationModelSerializer):
    class Meta(AdminPageSerializer.Meta):
        pass
