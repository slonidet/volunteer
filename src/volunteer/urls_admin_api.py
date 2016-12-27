from django.conf.urls import url, include


urlpatterns = [
    url(r'users/', include('users.urls_admin', namespace='users')),
    url(r'gallery/', include('gallery.urls_admin', namespace='gallery')),
    url(r'news/', include('news.urls_admin', namespace='news')),
    url(r'static/', include('static.urls_admin', namespace='static'))
]
