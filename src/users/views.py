from django.contrib.auth.models import Group
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.filters import UserFilter
from users.mixins import ExcludeAnonymousViewMixin, StoryRelatedViewMixin
from users.models import Profile, ProfileAttachment, Story, ProfileComment
from users.models import User
from users.serializers import ProfileSerializer, ProfileAttachmentSerializer, \
    AdminStorySerializer, StorySerializer, UserGroupSerializer, \
    ProfileCommentSerializer, ApproveProfileSerializer, AdminUserSerializer


class AdminUserViewSet(ExcludeAnonymousViewMixin, mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                       mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.select_related(
        'profile', 'profile_attachment').prefetch_related('groups').filter(
        is_superuser=False)
    serializer_class = AdminUserSerializer
    filter_class = UserFilter
    search_fields = ('username', 'profile__first_name', 'profile__last_name',
                     'profile__middle_name', 'profile__phone')


class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    filter_fields = ('user', 'status')
    search_fields = ('first_name', 'last_name', 'middle_name')

    @detail_route(methods=['get', 'post'],
                  serializer_class=ProfileCommentSerializer)
    def comments(self, request, pk=None):
        if request.method == 'GET':
            return self._comment_list(pk)
        if request.method == 'POST':
            return self._comment_create(request, pk)

    def _comment_list(self, pk):
        queryset = ProfileComment.objects.filter(profile_id=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProfileCommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProfileCommentSerializer(queryset, many=True)

        return Response(serializer.data)

    def _comment_create(self, request, pk):
        data = request.data
        profile = self.get_object()
        data['profile'] = profile.pk

        serializer = ProfileCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # set working profile status
        profile.status = Profile.STATUS_WORKING
        profile.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @detail_route(methods=['post'], serializer_class=ApproveProfileSerializer)
    def approve(self, request, pk=None):
        profile = self.get_object()
        serializer = ApproveProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            profile.user.profile_attachment
        except ProfileAttachment.DoesNotExist:
            raise exceptions.NotFound(_('Пользователь не загрузил фотографию'))

        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(pk=profile.pk)
            if serializer.validated_data['updated_at'] != profile.updated_at:
                raise exceptions.NotAcceptable(
                    _('Пользовательский профиль изменился, обновите страницу'))

            profile.status = Profile.STATUS_APPROVED
            profile.save()

        return Response(serializer.data)


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
    permission_classes = ()


class AdminUserGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = UserGroupSerializer
    pagination_class = None
