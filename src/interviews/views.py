from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from interviews.models import Interview


class InterviewPeriodView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(dict(Interview.PERIOD_CHOICES))


class InterviewStatusView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(dict(Interview.STATUS_CHOICES))
