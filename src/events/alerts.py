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
    day_forms = ['день', 'дня', 'дней']
    for event in events:
        users = event.users
        if event.is_actual:
            remaining = timezone.timedelta(event.start - timezone.now())
            if remaining in time_lapses:
                day_form = pluralization(remaining, day_forms)
                for user in users:
                    title = _('Напоминание о {}'.format(event.title))
                    message = _('До мероприятия {0} осталось {1} {2}'
                                .format(event.title, remaining, day_form))
                    Notice.objects.create(title=title,
                                          message=message,
                                          user=user,
                                          type=Notice.TYPE_ALERT,
                                          is_confirmed=None,
                                          )
