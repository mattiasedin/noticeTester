from django.core.management.base import BaseCommand, CommandError
from pusher.models import *

import kronos

@kronos.register('0 0 * * *')
class Command(BaseCommand):
    help = "My test command"

    def handle(self, *args, **options):
    	self.stdout.write("Doing All The Things!")