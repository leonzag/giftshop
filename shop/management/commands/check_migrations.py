from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """Django command to check for database migrations applied"""

    help = "Checks for database migrations applied"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM django_migrations")
            if not cursor.fetchone():
                raise RuntimeError("Migrations not applied")
