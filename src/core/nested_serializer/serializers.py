import random

from rest_framework import serializers


def get_negative_random_id(data_map):
    random_id = random.randint(-10000, -1)
    while random_id in data_map:
        random_id = random.randint(-10000, -1)
    return random_id


class NestedSerializerMixin(object):
    """
    Nested serializer mixin.

    You need mix serializer mixin to you serializer and view mixin to view
    at the same time. If you don't mix ReloadOnUpdateMixin after update or
    create you get response without your changes.

    Don't forget override Meta.m2m_nested_fields in serializer!

    m2m_nested_fields = ((parent_field, child_field), )
    """
    nested_data = None

    class Meta:
        nested_children_fields = ()

    def is_valid(self, raise_exception=False):
        # extract related objects before main validation
        # that would not validate nested objects
        self.nested_data = self._pop_related_objects(self.initial_data)

        return super().is_valid(raise_exception)

    def create(self, validated_data):
        instance = super().create(validated_data)

        if self.nested_data:
            self._create_nested(instance, self.nested_data)

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if self.nested_data:
            self._update_nested(instance, self.nested_data)

        return instance

    def _pop_related_objects(self, data):
        """ Pop all nested child objects from request data as noted in the
        ``m2m_nested_fields`` property.

        :param data: request data
        :return: dictionary in teh following form::

            {
                'parent_field': {
                    'child_field': <parent_fk_field>,
                    'data': [{<object 1 data>}, ...]
                }
            }
        """
        nested = {}
        for parent_field, child_field in self.Meta.nested_children_fields:
            if parent_field in data:
                child_data = data.pop(parent_field)
                child_data = child_data if isinstance(child_data, list) \
                    else [child_data]

                nested[parent_field] = {
                    'child_field': child_field,
                    'objects': child_data
                }

        return nested

    def _get_child_serializer(self, child_field):
        """ Get child serializer class from parent_model_name serializer. """
        try:
            return type(self.fields[child_field].child)
        except AttributeError:
            # if OneToOne relations
            return type(self.fields[child_field])

    @staticmethod
    def _validate_serializer(serializer):
        # TODO: костыль, после выхода 3.4.8 посмотреть решён ли баг
        # DRF parent-level validation of nested serializer bug
        # https://github.com/tomchristie/django-rest-framework/issues/4073
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(dict(e.detail))

    def _create_nested(self, parent_instance, nested_data):
        """ Create all children with """
        for parent_field, child_item in nested_data.items():
            child_serializer_class = self._get_child_serializer(parent_field)

            for data in child_item['objects']:
                data[child_item['child_field']] = str(parent_instance.pk)
                child_serializer = child_serializer_class(
                    data=data, context=self.context
                )

                self._validate_serializer(child_serializer)
                child_serializer.save()

    def _update_nested(self, parent_instance, nested_data):
        for parent_field, child_data in nested_data.items():
            try:
                child_instances = getattr(parent_instance, parent_field).all()
            except AttributeError:
                # if OneToOne relations
                child_instances = [getattr(parent_instance, parent_field)]

            child_serializer_class = self._get_child_serializer(parent_field)

            instance_mapping = {i.id: i for i in child_instances}

            data_mapping = {}
            for i in child_data['objects']:
                try:
                    i[child_data['child_field']] = parent_instance.pk
                    data_mapping[i['id']] = i
                except KeyError:
                    rand_id = get_negative_random_id(data_mapping)
                    data_mapping[rand_id] = i

            # update or create
            for object_id, data in data_mapping.items():
                instance = instance_mapping.get(object_id, None)

                if instance is None:
                    serializer = child_serializer_class(data=data)
                else:
                    serializer = child_serializer_class(
                        instance, data=data, partial=self.partial
                    )

                self._validate_serializer(serializer)
                serializer.save()

            # delete those not passed if PUT request
            if not self.partial:
                for object_id, instance in instance_mapping.items():
                    if object_id not in data_mapping:
                        instance.delete()


class M2MNestedSerializerMixin(object):
    m2m_nested_objects = {}

    class Meta:
        m2m_nested_fields = ()

    def is_valid(self, raise_exception=False):
        for field_name in self.Meta.m2m_nested_fields:
            nested_data = self.initial_data.pop(field_name, None)
            if not nested_data:
                continue

            nested_object_ids = [i.get('id', 0) for i in nested_data]
            nested_field = self.Meta.model._meta.get_field(field_name)
            related_model = nested_field.related_model
            self.m2m_nested_objects[field_name] = related_model.objects.filter(
                id__in=nested_object_ids
            )

        return super().is_valid(raise_exception)

    def create(self, validated_data):
        instance = super().create(validated_data)

        for field_name, nested_objects in self.m2m_nested_objects.items():
            getattr(instance, field_name).set(nested_objects)

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if self.partial:
            for field_name, nested_objects in self.m2m_nested_objects.items():
                getattr(instance, field_name).add(nested_objects)
        else:
            for field_name, nested_objects in self.m2m_nested_objects.items():
                getattr(instance, field_name).set(nested_objects)

        return instance
