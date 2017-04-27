from django.conf.urls import url, include

from core.views import SendMail
from volunteer.urls_view import api_root


urlpatterns = [
    url(r'^$', api_root, name='api-root'),

    # django social auth
    url(r'^social-auth/', include('social_auth.urls', namespace='social')),

    # admin api
    url(r'^admin/', include('volunteer.urls_admin_api', namespace='adm')),

    # public api
    url(r'^mail/(?P<email>[0-9a-z@.]+)/$', SendMail.as_view(), name='mail'),
    url(r'^user/', include('users.current.urls', namespace='user')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^static/', include('static.urls', namespace='static')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^tests/', include('user_tests.urls', namespace='tests')),
    url(r'^badges/', include('badges.urls', namespace='badges')),
    url(r'^notices/', include('notices.urls', namespace='notices')),
    url(r'^schedules/', include('schedules.urls', namespace='schedules')),
    url(r'^hall-of-fame/', include('hall_of_fame.urls', 'hall-of-fame')),
    url(r'^chats/', include('chats.urls', namespace='chats'))
]
