from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from social_core.utils import setting_name
from social_core.actions import do_complete
from social_django.utils import psa

NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'


@never_cache
@csrf_exempt
@psa('{0}:complete'.format(NAMESPACE))
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    do_complete(request.backend, _do_fake_login, request.user,
                redirect_name=REDIRECT_FIELD_NAME, *args, **kwargs)
    token = request.user.get_auth_token()

    return redirect('/?auth_token={0}'.format(token.key))


def _do_fake_login(backend, user, social_user):
    pass
