from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user': reverse('user:current-user', request=request, format=format),
        'user-authentication': reverse(
            'user:authentication', request=request, format=format),
        'user-registration': reverse(
            'user:registration', request=request, format=format),
        'user-activation': reverse(
            'user:activation', request=request, format=format,
            kwargs={'user_id': 1, 'token': 'tokentokentokentokentokentokento'}
        ),

        'users': reverse('users:user-list', request=request, format=format),
        'users-profiles': reverse(
            'users:profile-list', request=request, format=format),
        'users-profile-attachments': reverse(
            'users:profile-attachment-list', request=request, format=format),

        'gallery-photo-albums': reverse(
            'gallery:photo-album-list', request=request, format=format),
        'gallery-photos': reverse(
            'gallery:photo-list', request=request, format=format),
        'gallery-videos': reverse(
            'gallery:video-list', request=request, format=format),

        'news': reverse('news:news-list', request=request, format=format),
    })
