from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from flight.service.mock_airlines import MockAirlinesIncService, ValidationException
from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from airport.repository.iata_repository import IataRepository


class FlightsListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(
        self,
        request,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: str,
    ):
        mock_airline_api_connector = MockAirlineAPIConnector()
        iata_repository = IataRepository()
        flight_service = MockAirlinesIncService(
            mock_airline_api_connector, iata_repository
        )
        try:
            flight_combinations = flight_service.search_flights(
                origin=origin.upper(),
                destination=destination.upper(),
                departure_date=departure_date,
                return_date=return_date,
            )
            flight_combinations = [f.to_dict() for f in flight_combinations]
        except ValidationException as error:
            return Response({"error": str(error)}, 400)
        return Response(flight_combinations, 200)
