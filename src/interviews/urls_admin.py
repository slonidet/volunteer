from rest_framework import routers

from interviews.views import AdminInterviewerViewSet

router = routers.DefaultRouter()
router.register('interviewers', AdminInterviewerViewSet, 'interviewer')

urlpatterns = [] + router.urls
