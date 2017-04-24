from django.conf.urls import url, include


urlpatterns = [
    url(r'^users/', include('users.urls_admin', 'users')),
    url(r'^gallery/', include('gallery.urls_admin', 'gallery')),
    url(r'^news/', include('news.urls_admin', 'news')),
    url(r'^static/', include('static.urls_admin', 'static')),
    url(r'^events/', include('events.urls_admin', 'events')),
    url(r'^statistic/', include('statistic.urls_admin', namespace='statistic')),
    url(r'^interviews/', include('interviews.urls_admin', 'interviews')),
    url(r'^arbitrary-notices/', include(
        'notices.urls_admin', namespace='arbitrary-notices')),
    url(r'^tests/', include('user_tests.urls_admin', 'tests')),
    url(r'^schedules/', include('schedules.urls_admin', 'schedules')),
    url(r'^hall-of-fame/', include('hall_of_fame.urls_admin', 'hall-of-fame')),
]
