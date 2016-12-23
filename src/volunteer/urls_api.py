from django.conf.urls import url, include

from core.views import SendMail
from volunteer.urls_view import api_root


urlpatterns = [
    url(r'^$', api_root, name='api-root'),
    url(r'mail/(?P<email>[0-9a-z@.]+)/$', SendMail.as_view(), name='mail'),
    url(r'users/', include('users.urls', namespace='users')),
    url(r'user/', include('users.current.urls', namespace='user')),
    url(r'gallery/', include('gallery.urls', namespace='gallery')),
    url(r'news/', include('news.urls', namespace='news')),
]
