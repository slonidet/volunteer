from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from requests import HTTPError
from social_core.exceptions import AuthCanceled

from social_core.utils import setting_name, user_is_authenticated, \
    partial_pipeline_data, user_is_active
from social_django.utils import psa
from social_django.views import _do_login

NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'


@never_cache
@csrf_exempt
@psa('{0}:complete'.format(NAMESPACE))
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    try:
        user = do_complete(
            request.backend, _do_login, request.user, *args, **kwargs
        )
        token = user.get_auth_token()
    except (AuthCanceled, ValueError, HTTPError) as e:
        return redirect('/?error_message={0}'.format(
            _('Не удалось получить email для авторизации')
        ))

    return redirect('/?auth_token={0}'.format(token.key))


def do_complete(backend, login, user=None, *args, **kwargs):
    is_authenticated = user_is_authenticated(user)
    user = is_authenticated and user or None

    partial = partial_pipeline_data(backend, user, *args, **kwargs)
    if partial:
        user = backend.continue_pipeline(partial)
    else:
        user = backend.complete(user=user, *args, **kwargs)

    # check if the output value is something else than a user and just
    # return it to the client
    user_model = backend.strategy.storage.user.user_model()
    if user and not isinstance(user, user_model):
        return user

    elif user:
        if user_is_active(user):
            # catch is_new/social_user in case login() resets the instance
            social_user = user.social_user
            login(backend, user, social_user)
            # store last login backend name in session
            backend.strategy.session_set('social_auth_last_login_backend',
                                         social_user.provider)

    return user
