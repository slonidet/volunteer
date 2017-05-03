from django.core.management.base import BaseCommand, CommandError

from permission_manager.manager import set_permissions


class Command(BaseCommand):
    help = 'Set permissions'

    def handle(self, *args, **options):
        set_permissions()
