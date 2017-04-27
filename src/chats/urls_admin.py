from django.conf.urls import url

from chats.views import AdminTeamMessagesView

urlpatterns = [
    url(r'^$', AdminTeamMessagesView.as_view(), name='team-messages-list'),
]
