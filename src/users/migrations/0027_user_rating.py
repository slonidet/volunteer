# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-30 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_set_tested_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='рейтинг волонтера'),
        ),
    ]
