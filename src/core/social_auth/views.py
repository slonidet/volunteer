from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions


class SocialAuthLinksView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response({
            'twitter': reverse(
                'social:begin', kwargs={'backend': 'twitter'}
            )
        })
