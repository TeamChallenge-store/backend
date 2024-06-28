"""Django management command to wait until db is up and running."""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as psycopg2Error


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for db...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, psycopg2Error):
                self.stdout.write('Database not up, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database uppp!'))
