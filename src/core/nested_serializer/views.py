from rest_framework.response import Response


class ReloadOnUpdateMixin(object):
    """
    Mixin for retrieve updated response data
    """
    def update(self, request, *args, **kwargs):
        super(ReloadOnUpdateMixin, self).update(request, *args, **kwargs)
        serializer = self._reload_serializer_instance()

        return Response(serializer.data)

    def _reload_serializer_instance(self):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return serializer
