from abc import ABC, abstractmethod
from flight.entity.flight import Flight, FlightCombination


class IFlightAdapter(ABC):
    @abstractmethod
    def search_flights(
        self, origin: str, destination: str, departure_date: str, return_date: str
    ) -> list[FlightCombination]:
        pass

    @abstractmethod
    def transform_api_data(self, flight_data: dict | list) -> Flight:
        pass

    @abstractmethod
    def validate_parameters(
        self, origin: str, destination: str, departure_date: str, return_date: str
    ) -> None:
        pass
