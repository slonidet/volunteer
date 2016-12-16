from django.core.mail import send_mail
from rest_framework import views, permissions
from rest_framework.response import Response


class SendMail(views.APIView):
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, email):

        result = send_mail(
            'Subject test',
            'Here is the message.',
            'root@1m8.ru',
            [email],
            fail_silently=False,
        )

        return Response({'result': result})
