# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-24 08:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_auto_20170323_1739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participation',
            options={'default_permissions': ('view', 'add', 'change', 'delete')},
        ),
        migrations.AlterField(
            model_name='participation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set([('user', 'event')]),
        ),
    ]