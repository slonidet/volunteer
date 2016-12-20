from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _, ugettext
from rest_framework import views, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users.current.serializers import AuthUserSerializer
from users.current.tokens import RegisterTokenGenerator
from users.serializers import UserSerializer
from users.views import User


class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['current']
        user_serializer = AuthUserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'current': user_serializer.data,
            'token': token.key
        })


class UserActivationView(views.APIView):
    permission_classes = ()

    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)
        if RegisterTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()

        return redirect('/login')


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # deactivate current
        user.is_active = False
        user.save()

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