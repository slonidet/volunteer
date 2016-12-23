from rest_framework.generics import get_object_or_404


class CurrentUserViewMixin(object):
    """ Get objects only of the current user """
    user_pk_lookup_field = 'pk'

    def get_object(self):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        user_kwargs = {self.user_pk_lookup_field: user.pk}
        obj = get_object_or_404(queryset, **user_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj


class CurrentUserSerializerMixin(object):
    """ Create object only for current (request) user """
    class Meta:
        fields = None
        exclude = ('user', )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        return super().create(validated_data)