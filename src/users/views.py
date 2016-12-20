from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from users.models import Profile, ProfileAttachment
from users.serializers import (
    UserSerializer, ProfileSerializer, ProfileAttachmentSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(~Q(username='AnonymousUser'))
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.select_related('profile')

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        user = self.request.user

        if user.is_superuser:
            return qs

        return qs.filter(id=user.id)

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

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        user = self.request.user

        if user.is_superuser:
            return qs

        return qs.filter(user=user)


class ProfileAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ProfileAttachment.objects.all()
    serializer_class = ProfileAttachmentSerializer
    filter_fields = ('user', )

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        user = self.request.user

        if user.is_superuser:
            return qs

        return qs.filter(user=user)


