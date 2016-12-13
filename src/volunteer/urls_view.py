from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user-auth': reverse('users:auth', request=request, format=format),
        'users': reverse('users:user-list', request=request, format=format),
        'users-profiles': reverse('users:profile-list', request=request, format=format),
    })
