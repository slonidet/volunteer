# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='заголовок')),
                ('body', models.TextField(verbose_name='тело страницы')),
            ],
        ),
    ]