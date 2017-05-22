from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from hall_of_fame.models import HallOfFame
from hall_of_fame.serializers import HallOfFameSerializer, \
    AdminHallOfFameSerializer, AdminUsersHallOfFameSerializer
from users.models import User, Story


class AdminHallOfFameViewSet(ModelViewSet):
    queryset = HallOfFame.objects.all().select_related('user__profile')
    serializer_class = AdminHallOfFameSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['user']

        try:
            Story.objects.get(profile__user=user)
            return super().create(request, *args, **kwargs)
        except Story.DoesNotExist:
            raise exceptions.NotFound(
                _('У пользователя нет волонтерской истории'))


class AdminUsersHallOfFameViewSet(ModelViewSet):
    queryset = User.objects.select_related('profile')\
        .prefetch_related('hall_of_fame').exclude(
        role__in=(User.ROLE_REGISTERED, User.ROLE_CANDIDATE,))
    serializer_class = AdminUsersHallOfFameSerializer
    ordering_fields = ('rating', )


class HallOfFameView(ListAPIView):
    queryset = HallOfFame.objects.filter(is_published=True)\
        .select_related('user__profile')
    serializer_class = HallOfFameSerializer
    permission_classes = ()
