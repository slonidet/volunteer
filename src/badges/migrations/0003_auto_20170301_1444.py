# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-01 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0002_auto_20170228_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='type',
            field=models.CharField(choices=[('notice', 'нотификация'), ('profilecomment', 'Комментарий к анкете')], max_length=32, verbose_name='тип'),
        ),
    ]