# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-15 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_tests', '0006_auto_20170214_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=250, verbose_name='Текст вопроса'),
        ),
    ]
