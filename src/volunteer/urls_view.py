from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    params = {'request': request, 'format': format}

    return Response({
        'user': reverse('user:current-user', **params),
        'user-authentication': reverse('user:authentication', **params),
        'user-registration': reverse('user:registration', **params),
        'user-activation': reverse(
            'user:activation', **params,
            kwargs={'user_id': 1, 'token': 'tokentokentokentokentokentokento'}
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
