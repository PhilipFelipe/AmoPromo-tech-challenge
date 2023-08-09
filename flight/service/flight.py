from abc import ABC, abstractmethod

from flight.external.mock_airlines_inc_api import MockAirlineAPIConnector
from flight.utils.haversine_formula import haversine_distance
from flight.utils.calculate_flight_speed import (
    calculate_flight_speed,
    convert_str_to_datetime,
)
from flight.utils.calculate_cost_per_km import calculate_fare_per_km
from flight.utils.time import get_current_date
from airport.repository.iata_repository import IataRepository


class FlightLocationInfo:
    def __init__(
        self,
        iata_code: str,
        city: str,
        latitude: float,
        longitude: float,
        state: str,
    ):
        self.iata = iata_code
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.state = state

    def to_dict(self):
        return {
            "iata": self.iata,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "state": self.state,
        }


class FlightResumeInfo:
    def __init__(
        self,
        departure_date: str,
        currency: str,
        origin: FlightLocationInfo,
        destination: FlightLocationInfo,
    ):
        self.departure_date = departure_date
        self.currency = currency
        self.origin = origin
        self.destination = destination

    def to_dict(self):
        return {
            "departure_date": self.departure_date,
            "currency": self.currency,
            "origin": self.origin.__dict__,
            "destination": self.destination.__dict__,
        }


class PriceInfo:
    def __init__(self, fare, fees, total):
        self.fare = fare
        self.fees = fees
        self.total = total

    def to_dict(self):
        return {
            "fare": self.fare,
            "fees": self.fees,
            "total": self.total,
        }


class AircraftInfo:
    def __init__(self, model: str, manufacturer: str):
        self.model = model
        self.manufacturer = manufacturer

    def to_dict(self):
        return {
            "model": self.model,
            "manufacturer": self.manufacturer,
        }


class MetaInfo:
    def __init__(self, range: float, cruise_speed_kmh: float, cost_per_km: float):
        self.range = range
        self.cruise_speed_kmh = cruise_speed_kmh
        self.cost_per_km = cost_per_km

    def to_dict(self):
        return {
            "range": self.range,
            "cruise_speed_kmh": self.cruise_speed_kmh,
            "cost_per_km": self.cost_per_km,
        }


class FlightOptionsInfo:
    def __init__(
        self,
        departure_time: str,
        arrival_time: str,
        price: PriceInfo,
        aircraft: AircraftInfo,
        meta: MetaInfo,
    ):
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price
        self.aircraft = aircraft
        self.meta = meta

    def to_dict(self):
        return {
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "price": self.price.__dict__,
            "aircraft": self.aircraft.__dict__,
            "meta": self.meta.__dict__,
        }


class FlightInfo:
    def __init__(self, resume: FlightResumeInfo, options: list[FlightOptionsInfo]):
        self.resume = resume
        self.options = options

    def to_dict(self):
        return {
            "resume": self.resume.__dict__,
            "options": [option.__dict__ for option in self.options],
        }


class IFlightsIntegrationAdapter(ABC):
    @abstractmethod
    def search_flights(self) -> list:
        pass

    @abstractmethod
    def transform_api_data(self, *args, **kwargs) -> FlightInfo:
        pass


class MockAirlineIntegration(IFlightsIntegrationAdapter):
    def __init__(
        self,
        api_connector: MockAirlineAPIConnector,
        iata_repository: IataRepository,
    ):
        self.api_connector = api_connector
        self.iata_repository = iata_repository

    def validate_departure_date(self, departure_date: str):
        current_date = get_current_date()
        departure_datetime = convert_str_to_datetime(departure_date, format="%Y-%m-%d")
        if departure_datetime < current_date:
            return False
        return True

    def validate_arrival_date(self, departure_date: str, return_date: str):
        departure_datetime = convert_str_to_datetime(departure_date, format="%Y-%m-%d")
        arrival_datetime = convert_str_to_datetime(return_date, format="%Y-%m-%d")
        if arrival_datetime < departure_datetime:
            return False
        return True

    def validate_origin_and_destination(self, origin: str, destination: str):
        if origin == destination:
            return False
        return True

    def validate_origin_exists(self, origin: str):
        self.iata_repository.get_iata(iata=origin)

    def validate_destination_exists(self, destination: str):
        self.iata_repository.get_iata(iata=destination)

    def validate_parameters(
        self, origin: str, destination: str, departure_date: str, return_date: str
    ) -> tuple:
        is_valid = True
        msg = ""
        if not self.validate_origin_exists(origin):
            is_valid = (False,)
            msg = "Origin does not exist"
        if not self.validate_destination_exists(destination):
            is_valid = (False,)
            msg = "Destination does not exist"
        if not self.validate_origin_and_destination(origin, destination):
            is_valid = (False,)
            msg = "Origin and destination must be different"
        if not self.validate_departure_date(departure_date):
            is_valid = (False,)
            msg = "Departure date must be greater than current date"
        if not self.validate_arrival_date(departure_date, return_date):
            is_valid = (False,)
            msg = "Arrival date must be greater than departure date"
        return is_valid, msg

    def search_flights(
        self, origin: str, destination: str, departure_date: str, return_date: str
    ) -> list:
        is_valid, msg = self.validate_parameters(
            origin, destination, departure_date, return_date
        )
        if not is_valid:
            raise ValueError(msg)

        outbound_flight = self.api_connector.get_flights(
            origin, destination, departure_date
        )
        flight_back = self.api_connector.get_flights(destination, origin, return_date)
        standartized_outbound_flight = self.transform_api_data(outbound_flight)
        standartized_flight_back = self.transform_api_data(flight_back)
        flight_combinations = self.create_flight_combinations(
            outbound_flights=standartized_outbound_flight,
            flights_back=standartized_flight_back,
        )
        flight_combinations = sorted(flight_combinations, key=lambda k: k["price"])
        return flight_combinations

    def transform_api_data(self, flight: dict) -> FlightInfo:
        summary: dict = flight["summary"]
        origin = FlightLocationInfo(
            iata_code=summary["from"]["iata"],
            city=summary["from"]["city"],
            latitude=summary["from"]["lat"],
            longitude=summary["from"]["lon"],
            state=summary["from"]["state"],
        )
        destination = FlightLocationInfo(
            iata_code=summary["to"]["iata"],
            city=summary["to"]["city"],
            latitude=summary["to"]["lat"],
            longitude=summary["to"]["lon"],
            state=summary["to"]["state"],
        )
        flight_resume = FlightResumeInfo(
            departure_date=summary["departure_date"],
            currency=summary["currency"],
            origin=origin,
            destination=destination,
        )
        flight_options = []
        for option in flight["options"]:
            aircraft = AircraftInfo(
                model=option["aircraft"]["model"],
                manufacturer=option["aircraft"]["manufacturer"],
            )

            price = PriceInfo(
                fare=option["price"]["fare"],
                fees=option["price"]["fees"],
                total=option["price"]["total"],
            )
            self.fill_price_info(price)

            meta = MetaInfo(
                range=option["meta"]["range"],
                cruise_speed_kmh=option["meta"]["cruise_speed_kmh"],
                cost_per_km=option["meta"]["cost_per_km"],
            )
            self.fill_meta_info(
                meta=meta,
                flight_origin_locale=flight_resume.origin,
                flight_destination_locale=flight_resume.destination,
                departure_time=option["departure_time"],
                arrival_time=option["arrival_time"],
                price=price,
            )

            flight_options.append(
                FlightOptionsInfo(
                    departure_time=option["departure_time"],
                    arrival_time=option["arrival_time"],
                    price=price,
                    aircraft=aircraft,
                    meta=meta,
                )
            )

        flight_info = FlightInfo(
            resume=flight_resume,
            options=flight_options,
        )
        return flight_info

    def create_flight_combinations(
        self, outbound_flights: FlightInfo, flights_back: FlightInfo
    ) -> list:
        flight_combinations = []
        for outbound_flight in outbound_flights.options:
            for flight_back in flights_back.options:
                out_fli = outbound_flights.resume.to_dict()
                out_fli.update(outbound_flight.to_dict())
                fli_ba = flights_back.resume.to_dict()
                fli_ba.update(flight_back.to_dict())
                flight_combinations.append(
                    {
                        "price": outbound_flight.price.total + flight_back.price.total,
                        "outbound_flight": out_fli,
                        "flight_back": fli_ba,
                    }
                )

        return flight_combinations

    def fill_price_info(self, price: PriceInfo) -> PriceInfo:
        fee = round((10 / 100) * price.fare, 4)
        price.fees = fee if fee >= 40 else 40
        price.total = price.fare + price.fees
        return price

    def fill_meta_info(
        self,
        meta: MetaInfo,
        flight_origin_locale: FlightLocationInfo,
        flight_destination_locale: FlightLocationInfo,
        departure_time: str,
        arrival_time: str,
        price: PriceInfo,
    ) -> MetaInfo:
        distance_in_km = haversine_distance(
            lat1=flight_origin_locale.latitude,
            lon1=flight_origin_locale.longitude,
            lat2=flight_destination_locale.latitude,
            lon2=flight_destination_locale.longitude,
        )
        cruise_speed_kmh = calculate_flight_speed(
            distance=distance_in_km,
            arrival_time=arrival_time,
            departure_time=departure_time,
        )
        cost_per_km = calculate_fare_per_km(fare=price.fare, distance=distance_in_km)
        meta.range = distance_in_km
        meta.cruise_speed_kmh = cruise_speed_kmh
        meta.cost_per_km = cost_per_km
        return meta
