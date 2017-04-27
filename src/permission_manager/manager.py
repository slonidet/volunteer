from django.contrib.auth.models import Group, Permission
from permission_manager.group_permissions import PERMISSIONS


def set_permissions():
    for group_name, permission_data in PERMISSIONS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for permission in generate_permissions(permission_data):
            group.permissions.add(permission)


def generate_permissions(permission_data):
    for description in permission_data:
        model_name = description['model'].lower()
        app_label = description['app_label']

        for action in description['actions']:
            code_name = '{}_{}'.format(action, model_name)
            try:
                permission = Permission.objects.get_by_natural_key(
                    code_name, app_label, model_name,
                )
            except Permission.DoesNotExist:
                continue

            yield permission
