# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20170427_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='volunteer_limit',
            new_name='volunteers_limit',
        ),
        migrations.RemoveField(
            model_name='event',
            name='participants_count',
        ),
        migrations.RemoveField(
            model_name='event',
            name='volunteers_count',
        ),
    ]
