# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-23 12:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_auto_20170202_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('participant', 'participant'), ('volunteer', 'volunteer')], max_length=16, verbose_name='статус в мероприятии')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('event', 'событие'), ('forum', 'форум'), ('educational', 'образование')], default='event', max_length=16, verbose_name='тип мероприятия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='volunteer_count',
            field=models.PositiveSmallIntegerField(default=10, verbose_name='количество волонтеров'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participation',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
        migrations.AddField(
            model_name='participation',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(related_name='участники', through='events.Participation', to=settings.AUTH_USER_MODEL),
        ),
    ]
