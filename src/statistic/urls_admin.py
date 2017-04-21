from django.conf.urls import url

from statistic import views

urlpatterns = [
    url(r'main/$', views.AdminStatistic.as_view(), name='main'),
    url(r'profiles/gender-age/$', views.ProfileGenderAgeStatView.as_view(),
        name='profiles_gender_age'),
    url(r'profiles/geo/$', views.ProfileGeoStatistic.as_view(), name='profiles_geo'),
    url(r'profiles/interesting/$', views.ProfileInterestingStatistic.as_view(),
        name='profiles_interesting'),
    url(r'profiles/language/$', views.ProfileSecondLanguageStatistic.as_view(),
        name='profiles_language'),
]
