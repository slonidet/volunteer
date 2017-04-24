from collections import OrderedDict

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_root(request, format=None):
    params = {'request': request, 'format': format}
    links = {
        # Current User
        'user': reverse('user:current-user', **params),
        'user:authentication': reverse('user:authentication', **params),
        'user:registration': reverse('user:registration', **params),
        'user:activation': reverse(
            'user:activation', **params,
            kwargs={'user_id': 1, 'token': '76d80224611fc919a5d54f0ff9fba446'}
        ),
        'user:profile': reverse('user:current-user-profile', **params),
        'user:profile-attachment': reverse(
            'user:current-user-profile-attachment', **params),
        'user:profile:comments': reverse('user:current-user-profile-comments',
                                         **params),
        'user:story': reverse('user:current-user-story', **params),
        'user:reset-password': reverse('user:reset-password', **params),

        # Users
        'admin:users': reverse('adm:users:user-list', **params),
        'admin:users:profiles': reverse('adm:users:profile-list', **params),
        'admin:users:profiles:comments': reverse(
            'adm:users:profile-comments', **params, kwargs={'pk': 0}),
        'admin:users:profiles:approve': reverse(
            'adm:users:profile-approve', **params, kwargs={'pk': 0}),
        'admin:users:profile-attachments': reverse(
            'adm:users:profile-attachment-list', **params),
        'admin:users:stories': reverse('adm:users:story-list', **params),
        'admin:users:story-comments': reverse(
            'adm:users:story-comment-list', **params),
        'admin:users:groups': reverse('adm:users:group-list', **params),
        'admin:users:profession-city': reverse(
            'adm:users:profession_city-list', **params),
        'users:stories': reverse('users:story-list', **params),

        # Gallery
        'admin:gallery:photo-albums': reverse(
            'adm:gallery:photo-album-list', **params),
        'admin:gallery:photos': reverse('adm:gallery:photo-list', **params),
        'admin:gallery:videos': reverse('adm:gallery:video-list', **params),
        'gallery:photo-albums': reverse('gallery:photo-album-list', **params),
        'gallery:photos': reverse('gallery:photo-list', **params),
        'gallery:videos': reverse('gallery:video-list', **params),

        # News
        'admin:news': reverse('adm:news:news-list', **params),
        'news': reverse('news:news-list', **params),

        # User Tests
        'admin:users:tests': reverse('adm:tests:user-answer-list', **params),
        'admin:users:tests:average-score': reverse(
            'adm:tests:average-score-list', **params
        ),
        'tests': reverse('tests:test-list', **params),
        'tests:tasks': reverse('tests:task-list', **params),
        'tests:tasks:questions': reverse('tests:question-list', **params),
        'tests:tasks:questions:options': reverse('tests:option-list',
                                                 **params),
        'tests:user:tests': reverse('tests:user-test-list', **params),
        'tests:user:answers': reverse('tests:user-answer-list', **params),

        # Static pages
        'admin:static-pages': reverse('adm:static:page-list', **params),
        'static-pages': reverse('static:page-list', **params),

        # Events
        'admin:events': reverse('adm:events:event-list', **params),
        'events': reverse('events:event-list', **params),
        'events:participate': reverse(
            'events:event-participate', **params, kwargs={'pk': 0}
        ),

        # Badges
        'badges': reverse('badges:badge-list', **params),
        'badges:types': reverse('badges:types', **params),

        # Notices
        'notices': reverse('notices:notice-list', **params),
        'admin:notices:arbitrary-notices': reverse(
            'adm:arbitrary-notices:arbitrary-notices-list', **params),

        # Statistic
        'admin:statistic:main': reverse('adm:statistic:main', **params),
        'admin:statistic:profiles:gender_age': reverse(
            'adm:statistic:profiles_gender_age', **params),
        'admin:statistic:equipment': reverse('adm:statistic:equipment', **params),
        'admin:statistic:profiles:geo': reverse(
            'adm:statistic:profiles_geo', **params),
        'admin:statistic:profiles:interesting': reverse(
            'adm:statistic:profiles_interesting', **params),
        'admin:statistic:profiles:language': reverse(
            'adm:statistic:profiles_language', **params),
        'admin:statistic:users': reverse('adm:statistic:users', **params),

        # Social auth
        'social-auth:vk': reverse(
            'social:begin', **params, kwargs={'backend': 'vk-oauth2'}),
        'social-auth:facebook': reverse(
            'social:begin', **params, kwargs={'backend': 'facebook'}),
        'social-auth:twitter': reverse(
            'social:begin', **params, kwargs={'backend': 'twitter'}),
        'social-auth:mailru': reverse(
            'social:begin', **params, kwargs={'backend': 'mailru-oauth2'}),
        'social-auth:odnoklassniki': reverse(
            'social:begin', **params,
            kwargs={'backend': 'odnoklassniki-oauth2'}
        ),

        # Interviews
        'admin:interviews:interviewers': reverse(
            'adm:interviews:interviewer-list', **params),
        'admin:interviews': reverse('adm:interviews:interview-list', **params),
        'admin:interviews:periods': reverse('adm:interviews:period', **params),
        'admin:interviews:statuses': reverse('adm:interviews:status', **params),

        # schedules
        'schedules:shifts': reverse('schedules:shift-list', **params),
        'schedules:periods': reverse('schedules:period-list', **params),
        'schedules:user:schedule': reverse(
            'schedules:user-schedule-list', **params
        ),
        'schedules:team-leader:schedule': reverse(
            'schedules:team-leader-schedule-list', **params
        ),
        'admin:schedules:places': reverse(
            'adm:schedules:place-list', **params
        ),
        'admin:schedules:teams': reverse('adm:schedules:team-list', **params),
        'admin:schedules:user-position': reverse(
            'adm:schedules:user-position-list', **params
        ),
        'admin:schedules:relevant-users': reverse(
            'adm:schedules:relevant-user-list', **params
        ),
        'admin:schedules:user-position-statistics': reverse(
            'adm:schedules:user-position-statistic', **params
        ),

        # HallOfFame
        'hall_of_fame': reverse('hall_of_fame:hall_of_fame', **params),
        'admin:hall_of_fame': reverse(
            'adm:hall_of_fame:hall_of_fame-list', **params),

    }
    ordered_links = OrderedDict(sorted(links.items(), key=lambda x: x[0]))

    return Response(ordered_links)
