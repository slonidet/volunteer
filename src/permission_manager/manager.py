from django.contrib.auth.models import Group, Permission
from permission_manager.permissios_data import PERMISSIONS


def set_permissions():
    for group_name, descriptions in PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        import pdb; pdb.set_trace()
        for permission in generate_permissions(descriptions):
            group.permissions.add(permission)

def generate_permissions(descriptions):
    for description in descriptions:
        for action in description['actions']:
            code_name = '{}_{}'.format(action, description['model'])
            permission = Permission.objects.get_by_natural_key(
                codename=code_name,
                app_label=description['app_label'],
                model=description['model'],
            )
            yield permission
