from django.conf.urls import url

from statistic import views

urlpatterns = [
    url(r'main/$', views.AdminStatistic.as_view(), name='main'),
    url(r'profiles/gender-age$', views.ProfileGenderAgeStatView.as_view(),
        name='profiles_gender_age'),
    url(r'equipment/$', views.EquipmentStatistic.as_view(), name='equipment')
]
