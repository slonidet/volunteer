from social_core.pipeline.user import USER_FIELDS

from users.models import User


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return

    user = User.objects.filter(username=fields['email']).first()
    if not user:
        user = User.objects.create_user(username=fields['email'])

    return {
        'is_new': True,
        'user': user
    }