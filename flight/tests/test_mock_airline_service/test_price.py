from unittest import mock
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightservice.settings")

django.setup()

import pytest
from flight.service.mock_airlines import MockAirlinesIncService
from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from airport.repository.iata_repository import IataRepository


@pytest.fixture
def mock_airline_service() -> MockAirlinesIncService:
    return MockAirlinesIncService(MockAirlineAPIConnector(), IataRepository())


def test_build_price_fees_has_minimum_value_of_40(
    mock_airline_service: MockAirlinesIncService,
):
    price = mock_airline_service.build_price(fare=100, fees=0, total=0)
    assert price.fare == 100
    assert price.fees == 40  # 10% in this case should be 10 and the minimum fee is 40


def test_build_price_fees_is_equal_to_ten_percent_of_the_fare(
    mock_airline_service: MockAirlinesIncService,
):
    price = mock_airline_service.build_price(fare=525, fees=0, total=0)
    ten_percent = round(525 * 0.1, 4)
    assert price.fare == 525
    assert round(price.fees, 4) == ten_percent


def test_build_price_total_is_equal_to_fare_plust_fees(
    mock_airline_service: MockAirlinesIncService,
):
    price = mock_airline_service.build_price(fare=425, fees=0, total=0)
    assert price.total == price.fare + price.fees
