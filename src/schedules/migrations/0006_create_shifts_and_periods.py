# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-04 07:45
from __future__ import unicode_literals

from datetime import date, timedelta as delta

from django.db import migrations

from schedules.models import Shift, Period, Day


PERIODS_DAY_RANGE = {
    Period.FIRST: [date(2018, 6, 13) + delta(days=x) for x in range(0, 11)],
    Period.SECOND: [date(2018, 6, 24) + delta(days=x) for x in range(0, 11)],
    Period.THIRD: [date(2018, 7, 5) + delta(days=x) for x in range(0, 11)],
    Period.ANY: [],
}


def create_shifts_and_periods(apps, schema_editor):
    for system_name, name in Shift.CHOICES:
        Shift.objects.get_or_create(name=name, system_name=system_name)

    for system_name, name in Period.CHOICES:
        period, created = Period.objects.get_or_create(
            name=name, system_name=system_name
        )
        for day in PERIODS_DAY_RANGE.get(period.system_name):
            Day.objects.get_or_create(period=period, date=day)


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0005_auto_20170404_1044'),
    ]

    operations = [
        migrations.RunPython(create_shifts_and_periods)
    ]
