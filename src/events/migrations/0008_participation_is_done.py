# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-30 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20170327_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='is_done',
            field=models.BooleanField(default=False, verbose_name='пользователь присутствовал'),
        ),
    ]
