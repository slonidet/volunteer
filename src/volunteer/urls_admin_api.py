from django.conf.urls import url, include


urlpatterns = [
    url(r'^users/', include('users.urls_admin', namespace='users')),
    url(r'^gallery/', include('gallery.urls_admin', namespace='gallery')),
    url(r'^news/', include('news.urls_admin', namespace='news')),
    url(r'^static/', include('static.urls_admin', namespace='static')),
    url(r'^events/', include('events.urls_admin', namespace='events')),
    url(r'^statistic/', include('statistic.urls_admin', 'statistic')),
    url(r'^interviews/', include('interviews.urls_admin', 'interviews')),
    url(r'^tests/', include('user_tests.urls_admin', namespace='tests')),

]
