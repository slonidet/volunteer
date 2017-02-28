# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-28 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0003_auto_20170228_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='period',
            field=models.PositiveSmallIntegerField(choices=[(1, '09-10'), (2, '10-11'), (3, '11-12'), (4, '12-13'), (5, '13-14'), (6, '14-15'), (7, '15-16'), (8, '16-17'), (9, '17-18')], verbose_name='Время интервью'),
        ),
    ]