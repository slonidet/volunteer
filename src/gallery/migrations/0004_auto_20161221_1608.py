# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_remove_album_cover'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='name',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='name',
        ),
        migrations.AddField(
            model_name='photo',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='дата'),
        ),
    ]