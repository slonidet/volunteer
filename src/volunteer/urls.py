from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api'), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/',  # Adding login to the Browsable API
        include('rest_framework.urls', namespace='rest_framework')),

    url(r'^$', RedirectView.as_view(url='/api'), name='index'),

    # url(r'^api/', include('conf.urls_api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
