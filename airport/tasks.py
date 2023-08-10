from airport.service.airport_service import AirportService
from airport.external.domestic_airports_api import DomesticAirportAPIConnector
from airport.repository.airport_repository import AirportRepository
from airport.repository.iata_repository import IataRepository


class AirportTask:
    def __init__(self):
        self.airport_repository = AirportRepository(IataRepository())
        self.airport_service = AirportService(self.airport_repository)
        self.domestic_airport_api_connector = DomesticAirportAPIConnector()

    def update_airports(self):
        airports_data = self.domestic_airport_api_connector.retrieve_airports()
        self.airport_service.update_airports(airports_data)
