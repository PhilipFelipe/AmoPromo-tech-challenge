from django.core.management.base import BaseCommand
from airport.tasks import AirportTask


class Command(BaseCommand):
    help = "Process external airport API data and update the database"

    def handle(self, *args, **options):
        try:
            self.stdout.write(
                self.style.SUCCESS("Starting 'Domestic Airport API' data process")
            )
            AirportTask().update_airports()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"An error occurred during the 'Domestic Airport API' data process: {e}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS("Data from 'Domestic Airport API' procesing finished!")
        )
