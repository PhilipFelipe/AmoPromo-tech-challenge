from django.core.management.base import BaseCommand
from airport.tasks import AirportTask


class Command(BaseCommand):
    help = "Process external airport API daily at 6am"

    def handle(self, *args, **options):
        try:
            AirportTask().update_airports()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao processar dados da API: {e}"))

        self.stdout.write(self.style.SUCCESS("Dados da API processados com sucesso"))
