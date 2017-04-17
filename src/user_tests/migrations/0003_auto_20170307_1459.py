# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-07 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_tests', '0002_auto_20170221_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='expert_appraisal',
        ),
        migrations.AddField(
            model_name='task',
            name='evaluation_algorithm',
            field=models.CharField(choices=[('auto_appraisal', 'Проверяется автоматически'), ('expert_appraisal', 'Проверяется экспертом'), ('psychological', 'Задание психологического теста')], default='auto_appraisal', max_length=50, verbose_name='Алгоритм проверки'),
        ),
    ]