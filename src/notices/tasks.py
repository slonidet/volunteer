from celery import task

from notices.models import Notice


@task
def create_notifications(user_ids, msg, title):
    for user_id in user_ids:
        Notice.objects.create(
            type=Notice.TYPE_ALERT,
            message=msg,
            user_id=user_id, title=title,
            is_arbitrary=True,
        )
