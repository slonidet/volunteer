from django.conf.urls import url

from chats import views

urlpatterns = [
    url(r'^(?P<team_id>\d+)/$', views.TeamMessagesView.as_view(), name='team-messages-list'),
]
