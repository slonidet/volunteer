# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='заголовок')),
                ('body', models.TextField(verbose_name='текст')),
                ('date', models.DateField(auto_now_add=True, verbose_name='дата публикации')),
                ('is_public', models.BooleanField(default=False, verbose_name='опубликовано')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='фото')),
            ],
            options={
                'verbose_name_plural': 'новости',
                'verbose_name': 'новость',
            },
        ),
    ]
