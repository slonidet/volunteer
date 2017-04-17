# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-15 05:24
from __future__ import unicode_literals

from django.db import migrations

from user_tests.models import Test
from users.models import User as UserModel


def tested_role_data_migration(apps, schema_editor):
    User = apps.get_model("users", "User")

    finished_at_is_not_null = {'tests__finished_at__isnull': False}
    tested_users = User.objects.filter(
        tests__test__type=Test.TYPE_VERBAL, **finished_at_is_not_null
    ).filter(
        tests__test__type=Test.TYPE_NUMERICAL, **finished_at_is_not_null
    ).filter(
        tests__test__type=Test.TYPE_PSYCHOLOGICAL, **finished_at_is_not_null
    ).filter(
        tests__test__type=Test.TYPE_FOREIGN_LANGUAGE, **finished_at_is_not_null
    )

    tested_users.filter(role=UserModel.ROLE_APPROVED).update(
        role=UserModel.ROLE_TESTED
    )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_merge_20170302_1600'),
        ('user_tests', '0008_auto_20170315_0836'),
    ]

    operations = [
        migrations.RunPython(tested_role_data_migration)
    ]