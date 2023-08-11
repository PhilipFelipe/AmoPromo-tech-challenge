from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from airport.service.airport_service import AirportService
from airport.repository.airport_repository import AirportRepository
from airport.repository.iata_repository import IataRepository


class AirportListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        airport_repository = AirportRepository(IataRepository())
        airport_service = AirportService(airport_repository)
        airports = airport_service.get_airports()
        return Response(data=airports, status=200)
