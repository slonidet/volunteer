# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 07:56
from __future__ import unicode_literals

from django.db import migrations
from permissions import GROUPS


def replace_groups(apps, schema_editor):
    old_group_names = (
        'Волонтёр', 'Старший волонтёр', 'Координатор', 'Сотрудник',
        'Администратор'
    )

    Group = apps.get_model("auth", "Group")
    old_groups = Group.objects.filter(name__in=old_group_names)
    old_groups.delete()

    for group_name, display_name in GROUPS.items():
        Group.objects.create(name=group_name)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(replace_groups)
    ]
