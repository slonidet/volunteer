"""
Model translation serializer mixin
"""

from rest_framework import serializers
from django.conf import settings
from rest_framework.fields import empty


class BaseTranslationMixin(object):
    def __init__(self, instance=None, data=empty, **kwargs):
        if not self.Meta.model_translation:
            raise AttributeError(
                'You must define Meta.model_translation attribute')

        super().__init__(instance=instance, data=data, **kwargs)

    @staticmethod
    def get_translation_fields(languages, fields):
        translation_fields = []
        for field in fields:
            for lang in languages:
                translation_fields.append('{0}_{1}'.format(field, lang))

        return translation_fields


class AdminTranslationSerializerMixin(BaseTranslationMixin):
    """
    Translation serializer mixin for admin api
    """

    def get_field_names(self, declared_fields, info):
        """
        Hide original fields if using translation fields
        """
        fields = super().get_field_names(declared_fields, info)
        for field in self.Meta.model_translation.fields:
            fields.remove(field)

        return fields

    def get_extra_kwargs(self):
        """
        Mark all required translation fields as required in extra_kwargs
        """
        extra_kwargs = super().get_extra_kwargs()
        required_languages = self.Meta.model_translation.required_languages
        translation_fields = self.Meta.model_translation.fields

        required_fields = self.get_translation_fields(required_languages,
                                                      translation_fields)

        for field_name in required_fields:
            kwargs = extra_kwargs.get(field_name, {})
            kwargs['required'] = True
            extra_kwargs[field_name] = kwargs

        return extra_kwargs


class AdminTranslationModelSerializer(AdminTranslationSerializerMixin,
                                      serializers.ModelSerializer):
    pass


class UserTranslationSerializerMixin(BaseTranslationMixin):
    """
    Translation serializer mixin for user api
    """

    def get_field_names(self, declared_fields, info):
        """
        Hide translation fields for users serializers
        """
        fields = super().get_field_names(declared_fields, info)

        languages = [lang[0] for lang in settings.LANGUAGES]
        translation_fields = self.get_translation_fields(
            languages, self.Meta.model_translation.fields
        )
        for field in translation_fields:
            fields.remove(field)

        return fields


class UserTranslationModelSerializer(UserTranslationSerializerMixin,
                                     serializers.ModelSerializer):
    pass
