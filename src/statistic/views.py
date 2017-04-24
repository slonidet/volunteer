from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from events.models import Event
from gallery.models import Photo, Video
from users.models import User, Profile


class AdminPanelStatistic(generics.RetrieveAPIView):
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
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        time_measure = request.query_params.get('mesure', None)
        time_measure_number = request.query_params.get('number', None)

        if time_measure and time_measure_number:
            queryset = self.user_filtering_by_period(
                queryset, time_measure, time_measure_number
            )

        return Response({'number_of_users': queryset.count()})

    @staticmethod
    def user_filtering_by_period(queryset, time_measure, time_measure_number):
        time_measure_number = int(time_measure_number)
        time_measures = {
            'day': lambda x: x,
            'week': lambda x: x * 7,
            'month': lambda x: x * 30,
            'year': lambda x: x * 365,
        }

        days_number = time_measures.get(time_measure)(time_measure_number)
        begin = timezone.now() - timezone.timedelta(days=days_number)

        return queryset.filter(date_joined__gt=begin)


class EquipmentStatistic(generics.RetrieveAPIView):
    """
    Statistic about amount of equipment
    """
    queryset = Profile.objects.filter(user__role=User.ROLE_MAIN_TEAM)
    permission_classes = (permissions.IsAdminUser,)
    male_sizes = [size[0] for size in Profile.CLOTHES_SIZE_MALE_CHOICES]
    female_sizes = [size[0] for size in Profile.CLOTHES_SIZE_FEMALE_CHOICES]
    shoe_sizes = [size[0] for size in Profile.SHOE_SIZE_CHOICES]

    def get_sizes_array(self, gender=None, is_shoes=False):
        """
        Returns not associative array of numbers for every size.
        :param gender:
        :param is_shoes:
        :return:
        """
        final_list = []
        if is_shoes:
            for size in self.shoe_sizes:
                final_list.append(Profile.objects.filter(
                    shoe_size=size, user__role=User.ROLE_MAIN_TEAM).count())

            return final_list

        elif gender == Profile.GENDER_MALE:
            for size in self.male_sizes:
                final_list.append(Profile.objects.filter(
                    gender=Profile.GENDER_MALE,
                    clothes_size_male=size,
                    user__role=User.ROLE_MAIN_TEAM).count())

            return final_list

        elif gender == Profile.GENDER_FEMALE:
            for size in self.female_sizes:
                final_list.append(Profile.objects.filter(
                    gender=Profile.GENDER_FEMALE,
                    clothes_size_female=size,
                    user__role=User.ROLE_MAIN_TEAM).count())

            return final_list

    def retrieve(self, request, *args, **kwargs):
        equipment_data = {
            'male_clothes': {
                'male': self.get_sizes_array(gender=Profile.GENDER_MALE),
                'female': self.get_sizes_array(gender=Profile.GENDER_FEMALE)
            },
            'shoes': self.get_sizes_array(is_shoes=True)
        }

        return Response(equipment_data)
