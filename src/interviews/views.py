from rest_framework import permissions, views, viewsets
from rest_framework.response import Response

from core.views import UndeletableModelViewSet
from interviews.models import Interview, Interviewer
from interviews.serializers import InterviewerSerializer


class InterviewPeriodView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(dict(Interview.PERIOD_CHOICES))


class InterviewStatusView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(dict(Interview.STATUS_CHOICES))


class AdminInterviewerViewSet(UndeletableModelViewSet):
    queryset = Interviewer.objects.all()
    serializer_class = InterviewerSerializer
    pagination_class = None
