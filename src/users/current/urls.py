from django.conf.urls import url

from users.current import views


urlpatterns = [
    url(r'authentication/$', views.AuthTokenView.as_view(),
        name='authentication'),
    url(r'registration/$', views.UserRegistrationView.as_view(),
        name='registration'),
    url(r'activation/(?P<user_id>[0-9]+)/(?P<token>[a-z0-9]{32})/$',
        views.UserActivationView.as_view(), name='activation'),
]
