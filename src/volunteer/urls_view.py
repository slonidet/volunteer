from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes((permissions.IsAdminUser,))
def api_root(request, format=None):
    params = {'request': request, 'format': format}

    return Response({
        'user': reverse('user:current-user', **params),
        'user-authentication': reverse('user:authentication', **params),
        'user-registration': reverse('user:registration', **params),
        'user-activation': reverse(
            'user:activation', **params,
            kwargs={'user_id': 1, 'token': '76d80224611fc919a5d54f0ff9fba446'}
        ),
        'user-profile': reverse('user:current-user-profile', **params),
        'user-profile-attachment': reverse(
            'user:current-user-profile-attachment', **params),

        'users': reverse('users:user-list', **params),
        'users-profiles': reverse('users:profile-list', **params),
        'users-profile-attachments': reverse(
            'users:profile-attachment-list', **params),

        'gallery-photo-albums': reverse('gallery:photo-album-list', **params),
        'gallery-photos': reverse('gallery:photo-list', **params),
        'gallery-videos': reverse('gallery:video-list', **params),

        'news': reverse('news:news-list', **params),
    })
