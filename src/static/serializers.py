from rest_framework import serializers

from static.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'
        extra_kwargs = {
            'title_en': {'required': True},
            'body_en': {'required': True},
        }
