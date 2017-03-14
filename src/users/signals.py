from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from user_tests.models import UserTest, Test
from users.models import ProfileAttachment, Profile, User


@receiver(pre_delete, sender=ProfileAttachment)
def attachment_delete(sender, instance, **kwargs):
    """ Delete attachment from file system """
    instance.photo.delete(False)


@receiver(post_save, sender=User)
def set_default_user_group(sender, instance, created, **kwargs):
    if created:
        instance.set_default_group()


@receiver(post_save, sender=Profile)
def set_candidate_role_profile(sender, instance, created, **kwargs):
    """ Set user role as candidate if fill profile """
    if created:
        _set_candidate_role(instance, 'profile_attachment')


@receiver(post_save, sender=ProfileAttachment)
def set_candidate_role_attachment(sender, instance, created, **kwargs):
    """ Set user role as candidate if exist profile attachment """
    if created:
        _set_candidate_role(instance, 'profile')


def _set_candidate_role(instance, checked_model_field):
    user = instance.user
    if hasattr(user, checked_model_field):
        user.role = User.ROLE_CANDIDATE
        user.save()


@receiver(post_save, sender=Profile)
def set_approved_role(sender, instance, **kwargs):
    status = instance.status
    user = instance.user

    need_set_approved_role = (
        status == Profile.STATUS_APPROVED
        and user.role in (User.ROLE_CANDIDATE, User.ROLE_REGISTERED)
    )
    if need_set_approved_role:
        user.role = User.ROLE_APPROVED
        user.save()

    elif status != Profile.STATUS_APPROVED and user.role == User.ROLE_APPROVED:
        # rollback user approved role if admin change profile status
        user.role = User.ROLE_CANDIDATE
        user.save()


@receiver(post_save, sender=UserTest)
def set_tested_role(sender, instance, **kwargs):
    """ Set 'tested' role if user completed psychological, verbal, numeric
    and least one of the language tests """
    if instance.finished_at:
        not_foreign_language_tests = UserTest.objects.filter(
            user=instance.user,
            test__type__in=(
                Test.TYPE_PSYCHOLOGICAL, Test.TYPE_NUMERICAL, Test.TYPE_VERBAL)
        )

        if not_foreign_language_tests.count() == 3:
            foreign_language_tests = UserTest.objects.filter(
                user=instance.user, test__type=Test.TYPE_FOREIGN_LANGUAGE
            )

            if foreign_language_tests.exists():
                instance.user.role = User.ROLE_TESTED
                instance.user.save()
