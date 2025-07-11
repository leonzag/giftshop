import time

from django.core.management.base import BaseCommand, CommandError
from redis import Redis, RedisError


class Command(BaseCommand):
    """Django command to wait for Redis with timeout"""

    help = "Waits for Redis availability with timeout"

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")

    def handle(self, *args, **options):
        self.stdout.write("Waiting for Redis...")
        max_wait = options["timeout"]
        start = time.monotonic()

        while time.monotonic() - start < max_wait:
            try:
                Redis(host="redis", port=6379, db=0).ping()
                self.stdout.write(self.style.SUCCESS("Redis available!"))
                return
            except RedisError:
                self.stdout.write("Redis unavailable, waiting...")
                time.sleep(1)

        raise CommandError("Redis not available after 30s")
