# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 12:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20161221_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='cover',
        ),
    ]
