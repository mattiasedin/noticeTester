# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 15:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('push_notifications', '0002_auto_20160106_0850'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received', models.DateTimeField(verbose_name='Date recieved')),
                ('responded', models.DateTimeField(verbose_name='Date responded')),
                ('location', models.CharField(choices=[('H', 'HOME'), ('S', 'SCHOOL/UNIVERSITY'), ('W', 'WORK'), ('O', 'OTHER')], default='_', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], default='_', max_length=1)),
                ('occupation', models.CharField(choices=[('S', 'STUDENT'), ('E', 'EMPLOYED'), ('O', 'OTHER')], default='_', max_length=1)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='push_notifications.GCMDevice')),
            ],
        ),
        migrations.CreateModel(
            name='UserDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.CharField(max_length=255, unique=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deviceInfo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notificationdata',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pusher.Participant'),
        ),
    ]
