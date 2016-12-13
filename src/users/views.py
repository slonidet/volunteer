from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import Profile
from users.serializers import UserSerializer, ProfileSerializer

User = get_user_model()


class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'user': user.id, 'token': token.key})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(~Q(username='AnonymousUser'))
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.select_related('profile')

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
