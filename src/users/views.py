from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _, ugettext
from rest_framework import status
from rest_framework import viewsets, generics, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users.models import Profile
from users.serializers import (
    UserSerializer, ProfileSerializer,
    AuthUserSerializer)
from users.tokens import RegisterTokenGenerator

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


class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = AuthUserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': user_serializer.data,
            'token': token.key
        })


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        data = request.data
        # deactivate user
        data['is_active'] = False

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # send activation email
        token = RegisterTokenGenerator().make_token(user)
        activation_link = reverse(
            'users:activation', kwargs={'user_id': user.id, 'token': token},
            request=request
        )
        message = '{0}. {1}'.format(
            _('Для подтверждения регистрации пройдите по ссылке'),
            activation_link
        )
        user.email_user(subject=ugettext('Активация пользователя'),
                        message=message)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class UserActivationView(views.APIView):
    permission_classes = ()

    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)
        if RegisterTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()

        return redirect('/login')


class SendMail(views.APIView):
    def get(self, request, email):
        from django.core.mail import send_mail
        send_mail(
            'Subject here',
            'Here is the message.',
            'root@1m8.ru',
            [email],
            fail_silently=False,
        )
