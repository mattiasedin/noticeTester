# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pusher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received', models.DateTimeField(verbose_name='Date recieved')),
                ('responded', models.DateTimeField(verbose_name='Date responded')),
                ('namn', models.CharField(choices=[('H', 'HOME'), ('S', 'SCHOOL/UNIVERSITY'), ('W', 'WORK'), ('O', 'OTHER')], default='_', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceId', models.CharField(max_length=255, unique=True)),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], default='_', max_length=1)),
                ('occupation', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], default='_', max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='notificationdata',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pusher.Participant'),
        ),
    ]