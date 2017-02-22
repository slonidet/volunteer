from django.conf.urls import url
from rest_framework import routers

from interviews import views


router = routers.DefaultRouter()
# router.register('photo-album', AlbumViewSet, base_name='photo-album')


urlpatterns = [
    url(r'^periods/$', views.InterviewPeriodView.as_view(), name='period'),
    url(r'^statuses/$', views.InterviewStatusView.as_view(), name='status'),
] + router.urls
