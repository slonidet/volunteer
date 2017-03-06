from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import views, status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    get_object_or_404, CreateAPIView, RetrieveUpdateAPIView,
    ListAPIView, GenericAPIView)
from rest_framework.mixins import CreateModelMixin

from rest_framework.response import Response

from core.helpers import get_absolute_url
from users.current.mixins import CurrentUserViewMixin, \
    NotAllowEditApprovedProfileMixin
from users.current.serializers import AuthUserSerializer, \
    CurrentUserSerializer, CurrentUserProfileSerializer, \
    CurrentUserProfileAttachmentSerializer, CurrentUserStorySerializer, \
    ResetPasswordSerializer
from users.current.tokens import RegisterTokenGenerator
from users.models import Profile, ProfileAttachment, Story, ProfileComment
from users.serializers import ProfileCommentSerializer
from users.views import User
from users.mixins import StoryRelatedViewMixin
from volunteer import settings


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # deactivate current
        user.is_active = False
        user.save()

        user.send_activation_email(request)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class UserActivationView(views.APIView):
    permission_classes = ()

    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id, last_login=None)
        if RegisterTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()

        return redirect('/login')


class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = AuthUserSerializer(user)
        token = user.get_auth_token()

        return Response({
            'user': user_serializer.data,
            'token': token.key
        })


class CurrentUserView(CurrentUserViewMixin, RetrieveUpdateAPIView):
    queryset = User.objects.select_related(
        'profile', 'profile_attachment').prefetch_related('groups')
    serializer_class = CurrentUserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class BaseCurrentUserView(CurrentUserViewMixin, CreateModelMixin,
                          RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    user_pk_lookup_field = 'user__pk'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CurrentUserProfileView(NotAllowEditApprovedProfileMixin,
                             BaseCurrentUserView):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = CurrentUserProfileSerializer

    def perform_update(self, serializer):
        # set inspection status if user update profile
        serializer.validated_data['status'] = Profile.STATUS_INSPECTION
        super().perform_update(serializer)


class CurrentUserProfileAttachmentView(NotAllowEditApprovedProfileMixin,
                                       BaseCurrentUserView):
    queryset = ProfileAttachment.objects.select_related('user').all()
    serializer_class = CurrentUserProfileAttachmentSerializer


class CurrentUserProfileCommentView(ListAPIView):
    queryset = ProfileComment.objects.all()
    serializer_class = ProfileCommentSerializer
    user_pk_lookup_field = 'profile__user__pk'
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        user_kwargs = {self.user_pk_lookup_field: user.pk}

        return queryset.filter(**user_kwargs)


class CurrentUserStoryView(StoryRelatedViewMixin, BaseCurrentUserView):
    queryset = Story.objects.all()
    user_pk_lookup_field = 'profile__user__pk'
    serializer_class = CurrentUserStorySerializer

    def create(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=self.request.user).first()
        if not profile or profile.status != Profile.STATUS_APPROVED:
            raise exceptions.NotAcceptable(
                _('Нельзя создать волонтёрскую итосрию пока анкета '
                  'не утверждена администратором')
            )

        return super().create(request, args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_public:
            raise exceptions.PermissionDenied(
                _('Нельзя редактировать историю после публикации'))

        return super().update(request, *args, **kwargs)


class ResetPasswordView(GenericAPIView):
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            token = User.objects.get(username=email).get_auth_token()
            message = _('Для смены пароля перейдите по ссылке {0}?{1}')
            reset_link = get_absolute_url('/')
            result = send_mail(
                _('Сброс пароля на сайте городских волонтеров'),
                message.format(reset_link, token),
                settings.EMAIL_HOST_USER,
                [email],
            )

            return Response({'result': result})

        except ObjectDoesNotExist:
            error_message = _('Ползователь с данным e-mail не зарегистрирован')

            raise exceptions.NotFound(error_message)
