# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-05 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='is_arbitrary',
            field=models.BooleanField(default=False),
        ),
    ]
