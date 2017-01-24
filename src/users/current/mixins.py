from django.utils.translation import ugettext as _

from rest_framework import exceptions
from rest_framework.generics import get_object_or_404

from users.models import Profile


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
        exclude = ('id', 'user', )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        return super().create(validated_data)


class NotAllowEditApprovedProfileMixin(object):
    """ User can't edit profile if admin approve it """
    def perform_update(self, serializer):
        if serializer.instance.status == Profile.STATUS_APPROVED:
            raise exceptions.NotAcceptable(
                _('Нельзя редактировать утверждённую анкету')
            )

        super().perform_update(serializer)
