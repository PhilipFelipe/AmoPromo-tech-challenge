from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from flight.service.flight import MockAirlineIntegration
from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from airport.repository.iata_repository import IataRepository


class FlightsListAPIView(ListAPIView):
    def list(self, request, origin, destination, departure_date, return_date):
        mock_airline_api_connector = MockAirlineAPIConnector()
        iata_repository = IataRepository()
        flight_service = MockAirlineIntegration(
            mock_airline_api_connector, iata_repository
        )
        flight_combinations = flight_service.search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
        )
        return Response(flight_combinations, 200)
