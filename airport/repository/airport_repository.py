from abc import ABC, abstractmethod
from django.core.cache import cache
import logging

from airport.models import Airport, AirportSerializer
from airport.repository.iata_repository import IataRepository
from rest_framework.serializers import ReturnDict


class IAirportsRepository(ABC):
    @abstractmethod
    def get_airports(self) -> list:
        pass

    @abstractmethod
    def update_airports(self, airport_list: list[dict]) -> None:
        pass


class AirportRepository(IAirportsRepository):
    def __init__(self, iata_repository: IataRepository):
        self.iata_repository = iata_repository

    def get_airports(self) -> ReturnDict:
        cached_data = cache.get("airports")

        if cached_data is not None:
            logging.info("RETURNING CACHED AIRPORTS")
            return cached_data

        qs = Airport.objects.all()
        airports = AirportSerializer(qs, many=True).data
        cache.set("airports", airports, 60)
        logging.info("RETURNING FRESH AIRPORTS")
        return airports

    def update_airports(self, airport_list: list[dict]) -> None:
        for airport in airport_list:
            iata_obj = self.iata_repository.create_iata(airport["iata"])
            _, created = Airport.objects.update_or_create(
                iata=iata_obj,
                defaults={
                    "city": airport["city"],
                    "latitude": airport["latitude"],
                    "longitude": airport["longitude"],
                    "state": airport["state"],
                },
            )
            if created:
                logging.info("Airport created")

        cache.delete("airports")
        logging.info("Reseting cached airports data")
        return
