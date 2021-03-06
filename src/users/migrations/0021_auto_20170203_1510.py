# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-03 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20170201_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'default_permissions': ('view', 'add', 'change', 'delete'), 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата регистрации'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='активный'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='сотрудник'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.EmailField(max_length=254, unique=True, verbose_name='электронная почта'),
        ),
    ]
