from django.db.models.signals import post_save
from django.dispatch import receiver

from interviews.models import Interview
from notices.models import Notice


@receiver(post_save, sender=Notice)
def change_interview(sender, instance, **kwargs):
    """ Change interview status """
    notice = instance
    if isinstance(notice.content_object, Interview):
        interview = notice.content_object

        if notice.is_confirmed is True:
            interview.status = Interview.STATUS_CONFIRM
            interview.save()

        elif notice.is_confirmed is False:
            interview.status = Interview.STATUS_REJECT
            interview.save()


@receiver(post_save, sender=Interview)
def create_interview_notice(sender, instance, created, **kwargs):
    interview = instance
    if created:
        message = '{interviewer} пригласил вас на интервью {date} в {time}'
        Notice.objects.create(
            user=interview.volunteer,
            title='Приглашение на интервью',
            type=Notice.TYPE_CONFIRM,
            message=message.format(
                interviewer=interview.interviewer,
                date=interview.date.strftime('%d.%m.%Y'),
                time=interview.get_interview_time()
            ),
            content_object=interview
        )
