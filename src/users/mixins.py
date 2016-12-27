from django.db.models import Q


class ExcludeAnonymousViewMixin(object):
    def get_queryset(self):
        return super().get_queryset().filter(~Q(username='AnonymousUser'))


class StoryRelatedViewMixin(object):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'profile', 'profile__user'
        )
