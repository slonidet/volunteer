from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from core.helpers import pluralization
from events.models import Event
from notices.models import Notice
from volunteer.app_celery import app


@app.task(name='alert_users')
def alert_users():
    events = Event.objects.filter(is_public=True)
    time_lapses = (7, 3, 1)
    day_forms = _('день дня дней')

    for event in events:
        users = event.users
        if event.is_actual:
            remaining_time = event.start - timezone.now()
            remaining_days = remaining_time.days
            if remaining_days in time_lapses:
                day_form = pluralization(remaining_days, day_forms)
                for user in users:
                    title = _('Напоминание о {}'.format(event.title))
                    message = _('До мероприятия {0} осталось {1} {2}'
                                .format(event.title, remaining_days, day_form))
                    Notice.objects.create(
                        title=title, message=message, user=user,
                        type=Notice.TYPE_ALERT, is_confirmed=None,
                    )
