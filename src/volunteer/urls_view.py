from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_root(request, format=None):
    params = {'request': request, 'format': format}

    return Response({
        # Current User
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
        'user-profile-comments': reverse('user:current-user-profile-comments',
                                         **params),
        'user-story': reverse('user:current-user-story', **params),

        # Users
        'admin:users': reverse('adm:users:user-list', **params),
        'admin:users-profiles': reverse('adm:users:profile-list', **params),
        'admin:users-profiles-comments': reverse(
            'adm:users:profile-comments', **params, kwargs={'pk': 0}),
        'admin:users-profiles-approve': reverse(
            'adm:users:profile-approve', **params, kwargs={'pk': 0}),
        'admin:users-profile-attachments': reverse(
            'adm:users:profile-attachment-list', **params),
        'admin:users-stories': reverse('adm:users:story-list', **params),
        'admin:users-groups': reverse('adm:users:group-list', **params),
        'users-stories': reverse('users:story-list', **params),

        # Gallery
        'admin:gallery-photo-albums': reverse(
            'adm:gallery:photo-album-list', **params),
        'admin:gallery-photos': reverse('adm:gallery:photo-list', **params),
        'admin:gallery-videos': reverse('adm:gallery:video-list', **params),
        'gallery-photo-albums': reverse('gallery:photo-album-list', **params),
        'gallery-photos': reverse('gallery:photo-list', **params),
        'gallery-videos': reverse('gallery:video-list', **params),

        # News
        'admin:news': reverse('adm:news:news-list', **params),
        'news': reverse('news:news-list', **params),

        # Static pages
        'admin:static-pages': reverse('adm:static:page-list', **params),
        'static-pages': reverse('static:page-list', **params),
    })
