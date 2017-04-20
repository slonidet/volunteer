from django.db.models import Q, timezone
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from events.models import Event
from gallery.models import Photo, Video
from users.models import User, Profile


class AdminStatistic(generics.RetrieveAPIView):
    """ Statistic for admin panel """
    queryset = Profile.objects.all()

    def retrieve(self, request, *args, **kwargs):
        data = dict()
        data['profile_count'] = self.get_queryset().count()
        prepared_volunteer = (
            Q(role=User.ROLE_PREPARED) | Q(role=User.ROLE_MAIN_TEAM) |
            Q(role=User.ROLE_RESERVED)
        )
        data['volunteer_count'] = User.objects.filter(prepared_volunteer).count()
        data['event_count'] = Event.objects.all().count()
        data['photo_count'] = Photo.objects.all().count()
        data['video_count'] = Video.objects.all().count()

        return Response(data)


class UserStatistic(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        data = dict()

        return Response(3)

    def count_for_period(self, time_mesure, number):
        if time_mesure == 'day':
            since = timezone.now() - timezone.timedelta(days=number)





