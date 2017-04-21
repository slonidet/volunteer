# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-04 08:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0006_create_shifts_and_periods'),
        ('users', '0026_set_tested_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='work_period_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schedules.Period', verbose_name='период работы во время чемпионата'),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_shift_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schedules.Shift', verbose_name='смена работы во время чемпионата'),
        ),
    ]