import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightservice.settings")

django.setup()

import pytest
from flight.entity.flight import Option
from flight.service.mock_airlines import MockAirlinesIncService
from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from airport.repository.iata_repository import IataRepository


@pytest.fixture
def mock_airline_service() -> MockAirlinesIncService:
    return MockAirlinesIncService(MockAirlineAPIConnector(), IataRepository())


def test_extract_options_method_returns_list_of_options_object(
    mock_airline_service: MockAirlinesIncService,
):
    api_data = mock_airline_service.get_api_flight_data(
        origin="GRU",
        destination="STM",
        departure_date="2023-08-15",
    )
    options = mock_airline_service.extract_options(api_data)
    assert isinstance(options, list)
    assert all(isinstance(option, Option) for option in options)
