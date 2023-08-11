import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightservice.settings")

django.setup()

import pytest
from datetime import datetime, timedelta

from flight.service.mock_airlines import MockAirlinesIncService, ValidationException
from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from airport.repository.iata_repository import IataRepository


@pytest.fixture
def mock_airline_service() -> MockAirlinesIncService:
    return MockAirlinesIncService(MockAirlineAPIConnector(), IataRepository())


@pytest.fixture
def yesterday():
    yesterday_date = datetime.now() - timedelta(days=1)
    yesterday_date = yesterday_date.strftime("%Y-%m-%d")
    return yesterday_date


@pytest.fixture
def tomorrow():
    tomorrow_date = datetime.now() + timedelta(days=1)
    tomorrow_date = tomorrow_date.strftime("%Y-%m-%d")
    return tomorrow_date


def test_same_origin_and_destination_raises_exception(
    mock_airline_service: MockAirlinesIncService,
):
    with pytest.raises(ValidationException):
        mock_airline_service.validate_origin_and_destination(
            origin="GRU", destination="GRU"
        )


def test_invalid_origin_raises_exception(
    mock_airline_service: MockAirlinesIncService,
):
    with pytest.raises(ValidationException):
        mock_airline_service.validate_origin_exists(origin="GRUAAAAA")


def test_invalid_destination_raises_exception(
    mock_airline_service: MockAirlinesIncService,
):
    with pytest.raises(ValidationException):
        mock_airline_service.validate_destination_exists(destination="GRUAAAAA")


def test_invalid_departure_date_raises_exception(
    mock_airline_service: MockAirlinesIncService, yesterday: str
):
    with pytest.raises(ValidationException):
        mock_airline_service.validate_departure_date(departure_date=yesterday)


def test_invalid_return_date_raises_exception(
    mock_airline_service: MockAirlinesIncService, yesterday: str, tomorrow: str
):
    with pytest.raises(ValidationException):
        mock_airline_service.validate_return_date(
            departure_date=tomorrow, return_date=yesterday
        )
