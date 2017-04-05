from django.utils import timezone

from user_tests.models import UserTest
from volunteer.app_celery import app


@app.task(name='finish_expired_test')
def finish_expired_test():
    for test in UserTest.objects.filter(finished_at=None):
        if test.is_limited and test.remaining <= 0:
            test.finished_at = timezone.now()
            test.save()
