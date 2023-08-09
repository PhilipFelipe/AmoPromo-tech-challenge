from abc import ABC, abstractmethod
from airport.models import Iata, IataSerializer
from rest_framework.serializers import ReturnDict


class IIataRepository(ABC):
    @abstractmethod
    def get_iata(self) -> ReturnDict:
        pass

    @abstractmethod
    def create_iata(self, iata: str) -> None:
        pass


class IataRepository(IIataRepository):
    def get_iata(self, iata: str) -> ReturnDict:
        iata_obj = Iata.objects.filter(iata=iata).first()
        return IataSerializer(iata_obj).data

    def create_iata(self, iata: str) -> Iata:
        obj, created = Iata.objects.get_or_create(iata_code=iata)
        if not created:
            print("Iata already exists")
        return obj
