from django.conf.urls import url

from users.current import views


urlpatterns = [
    url(r'^$', views.CurrentUserViewView.as_view(),
        name='current-user'),
    url(r'authentication/$', views.AuthTokenView.as_view(),
        name='authentication'),
    url(r'registration/$', views.UserRegistrationView.as_view(),
        name='registration'),
    url(r'activation/(?P<user_id>[0-9]+)/(?P<token>[a-z0-9]{32})/$',
        views.UserActivationView.as_view(), name='activation'),
    url(r'profile/$', views.CurrentUserProfileView.as_view(),
        name='current-user-profile'),
    url(r'profile-attachment/$',
        views.CurrentUserProfileAttachmentView.as_view(),
        name='current-user-profile-attachment'),
    url(r'story/$', views.CurrentUserStoryView.as_view(),
        name='current-user-story'),
]
