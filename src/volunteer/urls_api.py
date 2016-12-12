from django.conf.urls import url, include

from volunteer.urls_view import api_root


urlpatterns = [
    url(r'^$', api_root, name='api-root'),
    url(r'users/', include('users.urls', namespace='users')),
]
