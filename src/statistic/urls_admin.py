from django.conf.urls import url

from statistic import views

urlpatterns = [
    url(r'main/$', views.AdminStatistic.as_view(), name='main'),
]
