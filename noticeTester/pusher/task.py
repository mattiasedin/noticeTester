from __future__ import absolute_import

from celery import shared_task
import datetime
import celery


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=5))
def myfunc():
    print 'periodic_task'