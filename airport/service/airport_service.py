from abc import ABC, abstractmethod

from airport.repository.airport_repository import IAirportsRepository


class IAirportsService(ABC):
    @abstractmethod
    def get_airports(self) -> list:
        pass

    @abstractmethod
    def update_airports(self) -> None:
        pass

    @abstractmethod
    def format_airport_data(self, airport_data: dict | list) -> list[dict]:
        pass


class AirportService(IAirportsService):
    def __init__(self, repository: IAirportsRepository):
        self.repository = repository

    def get_airports(self) -> list:
        return self.repository.get_airports()

    def update_airports(self, airports_data: dict) -> None:
        airports_list = self.format_airport_data(airports_data)
        return self.repository.update_airports(airports_list)

    def format_airport_data(self, airport_data: dict) -> list[dict]:
        airports_list = []
        for iata_code, airport_info in airport_data.items():
            airports_list.append(
                {
                    "iata": iata_code,
                    "city": airport_info["city"],
                    "latitude": airport_info["lat"],
                    "longitude": airport_info["lon"],
                    "state": airport_info["state"],
                }
            )
        return airports_list
