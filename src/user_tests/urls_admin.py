from django.conf.urls import url
from rest_framework import routers

from user_tests.views import AdminUserTestView


# router = routers.DefaultRouter()
# router.register('', AdminUserTestView, base_name='user-answer')


urlpatterns = [
    url(r'$', AdminUserTestView.as_view(), name='user-answer'),
              ]
