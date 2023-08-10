class Location:
    """This class is used to store the location of an airport"""

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


class Summary:
    """This class is used to store the summary of a flight"""

    def __init__(
        self,
        departure_date: str,
        currency: str,
        origin: Location,
        destination: Location,
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


class Price:
    """This class is used to store price data of a flight"""

    def __init__(self, fare, fees, total):
        self.fare = fare
        self.fees = fees
        self.total = total

    def to_dict(self):
        return {
            "fare": round(self.fare, 4),
            "fees": round(self.fees, 4),
            "total": round(self.total, 4),
        }


class Aircraft:
    """This class is used to store aircraft data of a flight"""

    def __init__(self, model: str, manufacturer: str):
        self.model = model
        self.manufacturer = manufacturer

    def to_dict(self):
        return {
            "model": self.model,
            "manufacturer": self.manufacturer,
        }


class Meta:
    """This class is used to store meta data of a flight"""

    def __init__(self, range: float, cruise_speed_kmh: float, cost_per_km: float):
        self.range = range
        self.cruise_speed_kmh = cruise_speed_kmh
        self.cost_per_km = cost_per_km

    def to_dict(self):
        return {
            "range": round(self.range, 4),
            "cruise_speed_kmh": round(self.cruise_speed_kmh, 4),
            "cost_per_km": round(self.cost_per_km, 4),
        }


class Options:
    """This class is used to store the flight options"""

    def __init__(
        self,
        departure_time: str,
        arrival_time: str,
        price: Price,
        aircraft: Aircraft,
        meta: Meta,
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


class Flight:
    """This class is used to store the flight data, which consists on a summary and a list of options"""

    def __init__(self, resume: Summary, options: list[Options]):
        self.resume = resume
        self.options = options

    def to_dict(self):
        return {
            "resume": self.resume.__dict__,
            "options": [option.__dict__ for option in self.options],
        }


class OutboundFlight:
    def __init__(self, resume: Summary, options: Options):
        self.flight_data = {}
        self.flight_data.update(resume.to_dict())
        self.flight_data.update(options.to_dict())


class FlightCombination:
    """This class is used to store the flight combination data, which consists on a outbound flight and a return flight"""

    def __init__(
        self,
        price: Price,
        outbound_flight: OutboundFlight,
        return_flight: OutboundFlight,
    ):
        self.price = price
        self.outbound_flight = outbound_flight
        self.return_flight = return_flight

    def to_dict(self):
        return {
            "price": self.price.to_dict(),
            "outbound_flight": self.outbound_flight.flight_data,
            "return_flight": self.return_flight.flight_data,
        }
