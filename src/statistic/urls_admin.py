from django.conf.urls import url

from statistic import views

urlpatterns = [
    url(r'main/$', views.AdminPanelStatistic.as_view(), name='main'),
    url(r'users/$', views.UserStatistic.as_view(), name='users'),
    url(r'equipment/$', views.EquipmentStatistic.as_view(), name='equipment')
]
