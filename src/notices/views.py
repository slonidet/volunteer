from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from notices.models import Notice
from notices.serializers import NoticeSerializer, ArbitraryNoticeSerializer
from users.models import User


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
    permission_classes = (permissions.IsAdminUser,)
    filter_fields = ('user__role',)
    allowed_roles = {choice[0] for choice in User.ROLE_CHOICES}

    def create(self, request, *args, **kwargs):
        choosed_roles = set(request.data['roles'])

        if choosed_roles <= self.allowed_roles:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            for role in choosed_roles:
                users_by_role = User.objects.filter(
                    role=role)

                for user in users_by_role:
                    Notice.objects.create(
                        type=Notice.TYPE_ALERT,
                        message=serializer.validated_data['message'],
                        user=user, title=serializer.validated_data['title'],
                        is_arbitrary=True,
                    )

            return Response(_('Нотификация отправленна'))

        else:
            raise ValidationError(_('Такой роли не существует'))
