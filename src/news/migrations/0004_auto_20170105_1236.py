# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 09:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20161228_0953'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'default_permissions': ('view', 'add', 'change', 'delete'), 'ordering': ('-date',), 'verbose_name': 'новость', 'verbose_name_plural': 'новости'},
        ),
    ]
