from rest_framework import routers

from news.views import NewsViewSet


router = routers.DefaultRouter()
router.register('', NewsViewSet, base_name='news')


urlpatterns = [] + router.urls
