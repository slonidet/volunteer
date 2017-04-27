from django.db import IntegrityError

from volunteer.app_celery import app
from notices.models import Notice


@app.task
def create_notifications(user_ids, msg, title):
    for user_id in user_ids:
        try:
            Notice.objects.create(
                type=Notice.TYPE_ALERT, message=msg, user_id=user_id,
                title=title, is_arbitrary=True
            )
        except IntegrityError:
            pass
