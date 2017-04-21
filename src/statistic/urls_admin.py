from django.conf.urls import url

from statistic import views

urlpatterns = [
    url(r'main/$', views.AdminStatistic.as_view(), name='main'),
    url(r'users/$', views.UserAnalytics.as_view(),
        name='users'),
]
