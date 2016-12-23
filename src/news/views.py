from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from news.models import News
from news.serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_fields = ('is_public',)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.has_module_perms('news'):
            queryset = queryset.filter(is_public=True)

        return queryset
