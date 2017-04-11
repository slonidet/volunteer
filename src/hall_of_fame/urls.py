from django.conf.urls import url

from hall_of_fame.views import HallOfFameView


urlpatterns = [
    url(r'hall_of_fame/$', HallOfFameView.as_view(), name='hall_of_fame'),
    ]
