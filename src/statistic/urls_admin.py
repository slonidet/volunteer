from django.conf.urls import url

from statistic import views

urlpatterns = [
    url(r'main/$', views.AdminStatistic.as_view(), name='main'),
    url(r'equipment/$', views.EquipmentStatistic.as_view(), name='equipment')
]
