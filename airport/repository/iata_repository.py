from abc import ABC, abstractmethod
from airport.models import Iata, IataSerializer
from rest_framework.serializers import ReturnDict
import logging


class IIataRepository(ABC):
    @abstractmethod
    def get_iata(self) -> ReturnDict:
        pass

    @abstractmethod
    def create_iata(self, iata: str) -> None:
        pass


class IataRepository(IIataRepository):
    def get_iata(self, iata: str) -> ReturnDict:
        iata_obj = Iata.objects.filter(iata_code=iata).first()
        return IataSerializer(iata_obj).data

    def create_iata(self, iata: str) -> Iata:
        obj, created = Iata.objects.get_or_create(iata_code=iata)
        if created:
            logging.info(f"Iata '{iata}' created.")
        return obj
