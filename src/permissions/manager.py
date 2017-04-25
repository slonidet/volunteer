from django.contrib.auth.models import Group, Permission


PERMISSIONS = {
    'group_1': [
        {'app_label': 'users', 'model': 'user', 'actions': ('view', 'add')},
    ],
}

for group_name, permissions in PERMISSIONS.items():
    group = Group.objects.get_or_create(name=group_name)

    for permission in permissions:
        for action in permission['actions']:
            code_name = '{}_{}'.format(action, permission['model'])
            permission = Permission.objects.get_by_natural_key(
                codename=code_name,
                app_label=permission['app_label'],
                model=permission['model'],
            )

            group.permissions.add(permission)
