from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

from push_notifications.models import GCMDevice


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserDevice(models.Model):
    owner = models.OneToOneField('auth.User', related_name='deviceInfo')
    deviceId = models.CharField(max_length=255, blank=False, unique=True)

class Participant(models.Model):
    #deviceId = models.CharField(max_length=255, blank=False, unique=True)
    device = models.OneToOneField(GCMDevice, related_name='participant', null=False, on_delete=models.CASCADE)

    age = models.IntegerField()

    GENDER_CHOICES = (
        ("M", "MALE"),
        ("F", "FEMALE"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, default="_")

    OCCUPATION_CHOICES = (
        ("S", "STUDENT"),
        ("E", "EMPLOYED"),
        ("O", "OTHER"),
    )

    occupation = models.CharField(max_length=1, choices=OCCUPATION_CHOICES, blank=False, default="_")

    def __unicode__(self):
        return str(self.age) + " Years, " + self.get_gender_display() + ", " + self.get_occupation_display()

class NotificationData(models.Model):
    owner = models.ForeignKey(Participant, null=False)
    server_sent = models.DateTimeField(verbose_name = 'Date sent')
    received = models.DateTimeField(verbose_name = 'Date recieved', null=True)
    responded = models.DateTimeField(verbose_name = 'Date responded', null=True)
    server_recieved = models.DateTimeField(verbose_name = 'Date sent', null=True)

    LOCATION_CHOICES = (
        ("H", "HOME"),
        ("S", "SCHOOL/UNIVERSITY"),
        ("W", "WORK"),
        ("O", "OTHER"),
    )
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES, blank=False, default="_")

    def __unicode__(self):
        return self.getTimeRecieved() + " - " + self.getTimeDiff()

    def getTimeRecieved(self, *args, **kwargs):
        if self.received:
            return str(self.received.hour) + ":" + str(self.received.minute) + ":" + str(self.received.second)
        return "nothing"
    def getTimeDiff(self, *args, **kwargs):
        if self.received and self.responded:
            timediff = self.responded - self.received 

            minutes = 0
            rest = timediff.total_seconds()

            while rest > 60:
                rest = rest - 60
                minutes = minutes + 1

            if minutes > 0:
                return str(minutes)+" minutes, "+str(int(rest))+" seconds"
            return str(int(rest))+" seconds"
        else:
            return "nothing"
    def getSecondDiff(self, *args, **kwargs):
        if self.responded and self.received:
            timediff = self.responded - self.received 
            return timediff.total_seconds()
        else:
            return -1

admin.site.register(Participant)
admin.site.register(NotificationData)