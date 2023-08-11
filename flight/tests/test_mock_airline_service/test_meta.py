import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightservice.settings")

django.setup()

import pytest
from flight.entity.flight import Location
from flight.service.mock_airlines import MockAirlinesIncService
from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from flight.utils.calculate_flight_speed import calculate_flight_speed
from flight.utils.calculate_cost_per_km import calculate_fare_per_km
from flight.utils.haversine_formula import haversine_distance
from airport.repository.iata_repository import IataRepository


@pytest.fixture
def mock_airline_service() -> MockAirlinesIncService:
    return MockAirlinesIncService(MockAirlineAPIConnector(), IataRepository())


@pytest.fixture
def distance_example():
    distance_in_km = haversine_distance(
        lat1=-23.425669,
        lon1=-46.481926,
        lat2=-2.424886,
        lon2=-54.78639,
    )
    return distance_in_km


@pytest.fixture
def cruise_speed_kmh_example(distance_example):
    cruise_speed_kmh = calculate_flight_speed(
        distance=distance_example,
        departure_time="2023-08-10T23:00:00",
        arrival_time="2023-08-11T09:00:00",
    )
    return cruise_speed_kmh


@pytest.fixture
def cost_per_km_example(distance_example, fare_example):
    cost_per_km = calculate_fare_per_km(fare=fare_example, distance=distance_example)
    return cost_per_km


@pytest.fixture
def fare_example():
    return 100


@pytest.fixture
def departure_date_example():
    return "2023-08-10T23:00:00"


@pytest.fixture
def arrival_date_example():
    return "2023-08-11T09:00:00"


def test_build_meta_cruise_speed_kmh_is_correct(
    mock_airline_service: MockAirlinesIncService,
    distance_example: float,
    cruise_speed_kmh_example: float,
    fare_example: float,
    departure_date_example: str,
    arrival_date_example: str,
):
    meta = mock_airline_service.build_meta(
        range=distance_example,
        cruise_speed_kmh=0,
        cost_per_km=0,
        departure_time=departure_date_example,
        arrival_time=arrival_date_example,
        fare=fare_example,
    )
    assert meta.cruise_speed_kmh == cruise_speed_kmh_example


def test_build_meta_cost_per_km_is_correct(
    mock_airline_service: MockAirlinesIncService,
    distance_example: float,
    fare_example: float,
    cost_per_km_example: float,
    departure_date_example: str,
    arrival_date_example: str,
):
    meta = mock_airline_service.build_meta(
        range=distance_example,
        cruise_speed_kmh=0,
        cost_per_km=0,
        departure_time=departure_date_example,
        arrival_time=arrival_date_example,
        fare=fare_example,
    )
    assert meta.cost_per_km == cost_per_km_example
