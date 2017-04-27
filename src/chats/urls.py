from django.conf.urls import url

from chats.views import TeamMessagesView

urlpatterns = [
    url(r'^(?P<team_id>\d+)/$', TeamMessagesView.as_view(), name='team-messages-list'),
]
