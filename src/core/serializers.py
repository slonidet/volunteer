from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class HyperlinkedSorlImageField(serializers.ImageField):
    """A Django REST Framework Field class returning hyperlinked scaled
    and cached images."""

    def __init__(self, geometry_string, options={}, *args, **kwargs):
        """
        Create an instance of the HyperlinkedSorlImageField image serializer.
        Args:
            geometry_string (str): The size of your cropped image.
            options (Optional[dict]): A dict of sorl options.
            *args: (Optional) Default serializers.ImageField arguments.
            **kwargs: (Optional) Default serializers.ImageField keyword
            arguments.
        For a description of sorl geometry strings and additional sorl options,
        please see
        https://sorl-thumbnail.readthedocs.org/en/latest/examples.html?highlight=geometry#low-level-api-examples
        """
        self.geometry_string = geometry_string
        self.options = options

        super(HyperlinkedSorlImageField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Perform the actual serialization.
        Args:
            value: the image to transform
        Returns:
            a url pointing at a scaled and cached image
        """
        if not value:
            return None

        image = get_thumbnail(value, self.geometry_string, **self.options)

        try:
            request = self.context.get('request', None)
            return request.build_absolute_uri(image.url)

        except:
            try:
                return super().to_representation(image.url)
            except AttributeError:
                return super().to_native(image.url)

    to_native = to_representation


class ForeignKeySerializerMixin(object):
    """
    Mixin for processing foreign key field serializers
    """
    class Meta:
        foreign_key_fields = ()

    def is_valid(self, raise_exception=False):
        # TODO: костыль, после выхода 3.4.8 посмотреть решён ли баг
        # DRF parent-level validation of nested serializer bug
        # https://github.com/tomchristie/django-rest-framework/issues/4073
        try:
            valid = super().is_valid(raise_exception=raise_exception)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(dict(e.detail))

        return valid

    def _prepare_foreign_key_fields(self, validated_data):
        for field in self.Meta.foreign_key_fields:
            ForeignModelClass = self.fields[field].Meta.model
            try:
                object_id = self.initial_data[field].get('id')
            except KeyError:
                return validated_data

            try:
                foreign_instance = ForeignModelClass.objects.get(id=object_id)
            except ForeignModelClass.DoesNotExist:
                raise serializers.ValidationError(
                    {'id': '{0} с id {1} не существует'.format(
                        ForeignModelClass._meta.model_name, object_id
                    )}
                )

            validated_data[field] = foreign_instance

        return validated_data

    def _foreign_key_unique_validation(self, validated_data):
        for fk_field_name in self.Meta.foreign_key_fields:
            ModelClass = self.Meta.model
            foreign_key_field = getattr(ModelClass, fk_field_name)

            if foreign_key_field.field.unique:
                try:
                    fk_field_id = validated_data[fk_field_name].pk
                    foreign_key_params = {fk_field_name: fk_field_id}

                    if ModelClass.objects.get(**foreign_key_params):
                        raise serializers.ValidationError(
                            {fk_field_name: 'Это поле должно быть уникально'}
                        )

                except (KeyError, ModelClass.DoesNotExist):
                    pass

    def create(self, validated_data):
        validated_data = self._prepare_foreign_key_fields(validated_data)
        self._foreign_key_unique_validation(validated_data)

        return super(ForeignKeySerializerMixin, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._prepare_foreign_key_fields(validated_data)

        return super(ForeignKeySerializerMixin, self).update(instance,
                                                             validated_data)
