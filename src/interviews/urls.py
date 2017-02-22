from django.conf.urls import url
from rest_framework import routers

from interviews.views import InterviewPeriodView, InterviewStatusView

router = routers.DefaultRouter()


urlpatterns = [
    url(r'^periods/$', InterviewPeriodView.as_view(), name='period'),
    url(r'^statuses/$', InterviewStatusView.as_view(), name='status'),
] + router.urls
