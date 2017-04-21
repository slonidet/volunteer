from django.db.models import Q
from django.db.models.functions import Length
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


class ProfileInterestingStatistic(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        count_all = self.queryset.count()
        tourist_information_values = self.queryset.filter(
            interesting_tourist_information=1).count()
        interesting_transportation_values = self.queryset.filter(
            interesting_transportation=1).count()
        interesting_language_values = self.queryset.filter(
            interesting_language=1).count()
        interesting_festival_values = self.queryset.filter(
            interesting_festival=1).count()
        data = dict()
        data['tourist_information_values'] = get_percentage(
            count_all, tourist_information_values)
        data['interesting_transportation_values'] = get_percentage(
            count_all, interesting_transportation_values)
        data['interesting_language_values'] = get_percentage(
            count_all, interesting_language_values)
        data['interesting_festival_values'] = get_percentage(
            count_all, interesting_festival_values)
        return Response(data)


class ProfileGenderAgeStatView(generics.RetrieveAPIView):
    """
    Show percentage for gender and age groups from user profiles
    """
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser, )

    count_males = Profile.objects.filter(gender=Profile.GENDER_MALE).count()
    count_females = Profile.objects.filter(
        gender=Profile.GENDER_FEMALE).count()
    count_all = count_males + count_females

    def retrieve(self, request, *args, **kwargs):
        data = dict()
        data['gender'] = self.get_gender_percentage()
        data['age'] = self.get_age_groups_percentage()
        return Response(data)

    def get_gender_percentage(self):
        genders_percents_dict = dict()
        genders_percents_dict['male'] = get_percentage(
            self.count_all, self.count_males)
        genders_percents_dict['female'] = get_percentage(
            self.count_all, self.count_females)

        return genders_percents_dict

    def get_age_groups_percentage(self):

        group_14_16 = tuple(range(14, 16))
        group_16_18 = tuple(range(16, 18))
        group_18_25 = tuple(range(18, 25))
        group_25_35 = tuple(range(25, 35))
        group_35_55 = tuple(range(35, 55))
        group_55_110 = tuple(range(55, 110))

        people_in_groups = {
            group_14_16: 0,
            group_16_18: 0,
            group_18_25: 0,
            group_25_35: 0,
            group_35_55: 0,
            group_55_110: 0,
        }
        ages_list = [profile.age for profile in Profile.objects.all()]
        ages_percents_dict = dict()

        for age_group in people_in_groups:
            for age in ages_list:
                if age in age_group:
                    people_in_groups[age_group] += 1
            key_string = str(age_group[0]) + '-' + str(age_group[-1])
            ages_percents_dict[key_string] = get_percentage(
                self.count_all, people_in_groups[age_group])

        return ages_percents_dict


class ProfileGeoStatistic(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        data = dict()
        data['foreigners'] = self.get_country_percentage()

        return Response(data)

    def get_country_percentage(self):
        count_all = self.queryset.count()
        number_of_russians = Profile.objects.annotate(
            passport_number_len=Length('passport_number')).filter(
            passport_number_len__gt=9).count()
        number_of_foreigners = count_all - number_of_russians

        return get_percentage(count_all, number_of_foreigners)


class ProfileSecondLanguageStatistic(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        data = dict()
        data['french'] = self.queryset.filter(
            Q(other_language__icontains='french') |
            Q(other_language__icontains='французский')).count()
        data['spanish'] = self.queryset.filter(
            Q(other_language__icontains='spanish') |
            Q(other_language__icontains='испанский')).count()
        data['german'] = self.queryset.filter(
            Q(other_language__icontains='german') |
            Q(other_language__icontains='немецкий')).count()
        data['italian'] = self.queryset.filter(
            Q(other_language__icontains='italian') |
            Q(other_language__icontains='итальянский')).count()
        data['japanese'] = self.queryset.filter(
            Q(other_language__icontains='japanese') |
            Q(other_language__icontains='японский')).count()
        data['chinese'] = self.queryset.filter(
            Q(other_language__icontains='chinese') |
            Q(other_language__icontains='mandarin') |
            Q(other_language__icontains='китайский')).count()
        data['ukrainian'] = self.queryset.filter(
            Q(other_language__icontains='ukrainian') |
            Q(other_language__icontains='украинский')).count()
        data['armenian'] = self.queryset.filter(
            Q(other_language__icontains='armenian') |
            Q(other_language__icontains='армянский')).count()
        data['portuguese'] = self.queryset.filter(
            Q(other_language__icontains='portuguese') |
            Q(other_language__icontains='португальский')).count()

        return Response(data)


def get_percentage(total, values):
    """
    Return percents proportion of value if 'value' is number. Returns dict of
    percents proportions of values if 'value' is list.
    :param total:
    :param values:
    :return: dict or number
    """
    return 100 * float(values) / float(total)
