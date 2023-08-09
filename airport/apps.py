from django.apps import AppConfig


class AirportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "airport"

    def ready(self) -> None:
        from airport.tasks import start_airport_job

        start_airport_job()
