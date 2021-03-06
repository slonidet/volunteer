# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static', '0002_auto_20161228_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='body_en',
            field=models.TextField(null=True, verbose_name='тело страницы'),
        ),
        migrations.AddField(
            model_name='page',
            name='body_ru',
            field=models.TextField(null=True, verbose_name='тело страницы'),
        ),
        migrations.AddField(
            model_name='page',
            name='title_en',
            field=models.CharField(max_length=512, null=True, verbose_name='заголовок'),
        ),
        migrations.AddField(
            model_name='page',
            name='title_ru',
            field=models.CharField(max_length=512, null=True, verbose_name='заголовок'),
        ),
    ]
