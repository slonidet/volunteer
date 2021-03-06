from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from notices.models import Notice
from notices.serializers import NoticeSerializer, ArbitraryNoticeSerializer
from users.models import User
from notices.tasks import create_notifications


class NoticeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.ListModelMixin, GenericViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ArbitraryNoticeViewSet(ModelViewSet):
    queryset = Notice.objects.filter(is_arbitrary=True)
    serializer_class = ArbitraryNoticeSerializer
    filter_fields = ('user__role',)
    allowed_roles = {choice[0] for choice in User.ROLE_CHOICES}

    def create(self, request, *args, **kwargs):
        try:
            chosen_roles = set(request.data.get('roles', None))
        except TypeError:
            raise ValidationError(_('Не переданы "roles"'))

        if not chosen_roles.issubset(self.allowed_roles):
            raise ValidationError(_('Такой роли не существует'))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids_by_role = [obj['id'] for obj in User.objects.filter(
            role__in=chosen_roles).values('id')]

        create_notifications.delay(
            user_ids_by_role,
            serializer.validated_data['message'],
            serializer.validated_data['title']
        )

        return Response(_('Нотификация отправленна'))
