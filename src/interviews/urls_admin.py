from django.conf.urls import url
from rest_framework import routers

from interviews.views import AdminInterviewerViewSet, AdminInterviewViewSet, \
    InterviewPeriodView, InterviewStatusView

router = routers.DefaultRouter()
router.register('interviewers', AdminInterviewerViewSet, 'interviewer')
router.register('', AdminInterviewViewSet, 'interview')

urlpatterns = [
    url(r'^periods/$', InterviewPeriodView.as_view(), name='period'),
    url(r'^statuses/$', InterviewStatusView.as_view(), name='status'),
] + router.urls
