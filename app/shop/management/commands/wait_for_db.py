import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database with timeout"""

    help = "Waits for database availability with timeout"

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        max_wait = options["timeout"]
        start = time.monotonic()

        while time.monotonic() - start < max_wait:
            try:
                connection.ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        raise CommandError(f"Database not available after {max_wait}s")
