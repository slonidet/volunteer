from django.utils.translation import ugettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.response import Response

from users.mixins import ExcludeAnonymousViewMixin
from users.models import Profile, ProfileAttachment
from users.models import User
from users.serializers import (
    UserSerializer, ProfileSerializer, ProfileAttachmentSerializer
)


class UserViewSet(ExcludeAnonymousViewMixin, viewsets.ModelViewSet):
    queryset = User.objects.select_related('profile')
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            message = _(
                'Нельзя удалить пользователя с правами супер-администратора'
            )
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    filter_fields = ('user', )


class ProfileAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ProfileAttachment.objects.all()
    serializer_class = ProfileAttachmentSerializer
    filter_fields = ('user', )


