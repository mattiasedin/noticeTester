from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserData(models.Model):
	user = models.OneToOneField(User)
	deviceID = models.CharField(max_length=255, blank=False, default='')


class notificationData(models.Model):
	user = models.ForeignKey(User)
	timeDelta = models.PositiveIntegerField(default=0)

	LOW = 0
	NORMAL = 1
	HIGH = 2

	STATUS_CHOICES = (
	    (LOW, 'Low'),
	    (NORMAL, 'Normal'),
	    (HIGH, 'High'),
	)

	stresslevel = models.PositiveIntegerField(choices=STATUS_CHOICES, default=0)