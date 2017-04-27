from django.conf.urls import url

from statistic.views import AdminPanelStatistic, UserStatistic, \
    EquipmentStatistic, ProfileGenderAgeStatView, ProfileGeoStatistic, \
    ProfileInterestingStatistic, ProfileSecondLanguageStatistic, \
    ProfileEnglishLanguageStatistic


urlpatterns = [
    url(r'main/$', AdminPanelStatistic.as_view(), name='main'),
    url(r'users/$', UserStatistic.as_view(), name='users'),
    url(r'equipment/$', EquipmentStatistic.as_view(), name='equipment'),
    url(r'main/$', AdminPanelStatistic.as_view(), name='main'),
    url(r'profiles/gender-age/$', ProfileGenderAgeStatView.as_view(),
        name='profiles_gender_age'),
    url(r'profiles/geo/$', ProfileGeoStatistic.as_view(),
        name='profiles_geo'),
    url(r'profiles/interesting/$', ProfileInterestingStatistic.as_view(),
        name='profiles_interesting'),
    url(r'profiles/language/$', ProfileSecondLanguageStatistic.as_view(),
        name='profiles_language'),
    url(r'profiles/english/$', ProfileEnglishLanguageStatistic.as_view(),
        name='profiles_english'),
]
