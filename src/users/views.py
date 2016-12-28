from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.mixins import ExcludeAnonymousViewMixin, StoryRelatedViewMixin
from users.models import Profile, ProfileAttachment, Story
from users.models import User
from users.serializers import (
    UserSerializer, ProfileSerializer, ProfileAttachmentSerializer,
    AdminStorySerializer, StorySerializer,
    UserGroupSerializer)


class AdminUserViewSet(ExcludeAnonymousViewMixin, viewsets.ModelViewSet):
    queryset = User.objects.select_related(
        'profile', 'profile_attachment').prefetch_related('groups')
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


class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    filter_fields = ('user', )


class AdminProfileAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ProfileAttachment.objects.all()
    serializer_class = ProfileAttachmentSerializer
    filter_fields = ('user', )


class AdminStoryViewSet(StoryRelatedViewMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, mixins.ListModelMixin,
                        GenericViewSet):
    queryset = Story.objects.all()
    serializer_class = AdminStorySerializer
    filter_fields = ('is_public', )


class StoryViewSet(StoryRelatedViewMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Story.objects.filter(is_public=True)
    serializer_class = StorySerializer


class AdminUserGroupViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                            mixins.ListModelMixin, GenericViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = UserGroupSerializer
