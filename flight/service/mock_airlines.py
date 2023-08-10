from flight.utils.haversine_formula import haversine_distance
from flight.utils.calculate_flight_speed import (
    calculate_flight_speed,
    convert_str_to_datetime,
)
from flight.utils.calculate_cost_per_km import calculate_fare_per_km
from flight.utils.time import get_current_date
from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from airport.repository.iata_repository import IataRepository
from flight.entity.flight import (
    Flight,
    Location,
    OutboundFlight,
    Summary,
    Price,
    Aircraft,
    Meta,
    Options,
    FlightCombination,
)
from flight.service.flight_adapter import IFlightAdapter


class ValidationException(Exception):
    pass


class MockAirlinesIncService(IFlightAdapter):
    def __init__(
        self,
        api_connector: MockAirlineAPIConnector,
        iata_repository: IataRepository,
    ):
        self.api_connector = api_connector
        self.iata_repository = iata_repository

    def search_flights(
        self, origin: str, destination: str, departure_date: str, return_date: str
    ) -> list[FlightCombination]:
        self.validate_parameters(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
        )
        outbound_flight_data = self.get_api_flight_data(
            origin=origin, destination=destination, departure_date=departure_date
        )
        return_flight_data = self.get_api_flight_data(
            origin=destination, destination=origin, departure_date=return_date
        )
        formatted_outbound_flight_data = self.transform_api_data(
            flight_data=outbound_flight_data
        )
        formatted_return_flight_data = self.transform_api_data(
            flight_data=return_flight_data
        )
        flight_combinations = self.mount_flight_combination(
            outbound_flights=formatted_outbound_flight_data,
            return_flights=formatted_return_flight_data,
        )
        flight_combinations = sorted(flight_combinations, key=lambda k: k.price)
        return flight_combinations

    def transform_api_data(self, flight_data: dict) -> Flight:
        summary = self.extract_summary(flight_data)
        flight_options = self.extract_options(flight_data)
        flight = Flight(
            resume=summary,
            options=flight_options,
        )
        return flight

    def get_api_flight_data(
        self, origin: str, destination: str, departure_date: str
    ) -> dict:
        return self.api_connector.get_flights(origin, destination, departure_date)

    def extract_summary(self, flight_data: dict) -> Summary:
        summary_data: dict = flight_data["summary"]
        origin = Location(
            iata_code=summary_data["from"]["iata"],
            city=summary_data["from"]["city"],
            latitude=summary_data["from"]["lat"],
            longitude=summary_data["from"]["lon"],
            state=summary_data["from"]["state"],
        )
        destination = Location(
            iata_code=summary_data["to"]["iata"],
            city=summary_data["to"]["city"],
            latitude=summary_data["to"]["lat"],
            longitude=summary_data["to"]["lon"],
            state=summary_data["to"]["state"],
        )
        return Summary(
            departure_date=summary_data["departure_date"],
            currency=summary_data["currency"],
            origin=origin,
            destination=destination,
        )

    def extract_options(self, flight_data: dict) -> list[Options]:
        options = flight_data["options"]
        summary = flight_data["summary"]

        flight_options = []
        for option in options:
            aircraft = Aircraft(
                model=option["aircraft"]["model"],
                manufacturer=option["aircraft"]["manufacturer"],
            )
            price = self.build_price(
                fare=option["price"]["fare"],
                fees=option["price"]["fees"],
                total=option["price"]["total"],
            )
            meta = self.build_meta(
                range=option["meta"]["range"],
                cruise_speed_kmh=option["meta"]["cruise_speed_kmh"],
                cost_per_km=option["meta"]["cost_per_km"],
                distance_in_km=haversine_distance(
                    summary["from"]["lat"],
                    summary["from"]["lon"],
                    summary["to"]["lat"],
                    summary["to"]["lon"],
                ),
                departure_time=option["departure_time"],
                arrival_time=option["arrival_time"],
                fare=price.fare,
            )

            flight_options.append(
                Options(
                    departure_time=option["departure_time"],
                    arrival_time=option["arrival_time"],
                    price=price,
                    aircraft=aircraft,
                    meta=meta,
                )
            )
        return flight_options

    def mount_flight_combination(
        self, outbound_flights: Flight, return_flights: Flight
    ) -> list[FlightCombination]:
        flight_combinations = []
        for outbound_flight in outbound_flights.options:
            for flight_back in return_flights.options:
                flight_combination = FlightCombination(
                    price=outbound_flight.price.total + flight_back.price.total,
                    outbound_flight=OutboundFlight(
                        outbound_flights.resume, outbound_flight
                    ),
                    return_flight=OutboundFlight(return_flights.resume, flight_back),
                )
                flight_combinations.append(flight_combination)

        return flight_combinations

    def build_price(self, fare: float, fees: float = 0, total: float = 0) -> Price:
        """Method used to build the price object based on the fare, filling up the fees and total"""
        price = Price(fare, fees, total)

        # Calculates the fees based on established rule
        fee = round((10 / 100) * price.fare, 4)
        price.fees = max(fee, 40)  # Make sure the fee is not less than 40
        price.total = price.fare + price.fees
        return price

    def build_meta(
        self,
        range: float,
        cruise_speed_kmh: float,
        cost_per_km: float,
        distance_in_km: float,
        departure_time: str,
        arrival_time: str,
        fare: float,
    ) -> Meta:
        """Method used to build the meta object and fullfill the range, cruise_speed_kmh and cost_per_km"""
        meta = Meta(range, cruise_speed_kmh, cost_per_km)

        cruise_speed = calculate_flight_speed(
            distance=distance_in_km,
            arrival_time=arrival_time,
            departure_time=departure_time,
        )
        cost = calculate_fare_per_km(fare=fare, distance=distance_in_km)

        meta.cruise_speed_kmh = cruise_speed
        meta.cost_per_km = cost
        return meta

    def validate_parameters(
        self, origin: str, destination: str, departure_date: str, return_date: str
    ):
        self.validate_origin_exists(origin)
        self.validate_destination_exists(destination)
        self.validate_origin_and_destination(origin, destination)
        self.validate_departure_date(departure_date)
        self.validate_arrival_date(departure_date, return_date)

    def validate_origin_exists(self, origin: str):
        iata_info = self.iata_repository.get_iata(iata=origin)
        if not iata_info["iata_code"]:
            raise ValidationException("Origin does not exist")

    def validate_destination_exists(self, destination: str):
        iata_info = self.iata_repository.get_iata(iata=destination)
        if not iata_info["iata_code"]:
            raise ValidationException("Destination does not exist")

    def validate_origin_and_destination(self, origin: str, destination: str):
        if origin == destination:
            raise ValidationException("Origin and destination must be different")

    def validate_departure_date(self, departure_date: str):
        current_date = get_current_date()
        departure_datetime = convert_str_to_datetime(departure_date, format="%Y-%m-%d")
        if departure_datetime.date() < current_date.date():
            raise ValidationException(
                "Departure date must be greater than current date"
            )

    def validate_arrival_date(self, departure_date: str, return_date: str):
        departure_datetime = convert_str_to_datetime(departure_date, format="%Y-%m-%d")
        arrival_datetime = convert_str_to_datetime(return_date, format="%Y-%m-%d")
        if arrival_datetime.date() < departure_datetime.date():
            raise ValidationException(
                "Arrival date must be greater than departure date"
            )
