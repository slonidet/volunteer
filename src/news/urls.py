from rest_framework import routers

from news.views import NewsViewSet, PublicNewsViewSet


router = routers.DefaultRouter()
router.register('news', NewsViewSet, base_name='news')
router.register('news-public', PublicNewsViewSet, base_name='news-public')


urlpatterns = [] + router.urls
