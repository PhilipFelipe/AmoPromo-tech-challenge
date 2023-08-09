from datetime import datetime


def convert_str_to_datetime(date_str: str, format: str | None = None) -> datetime:
    date = datetime.strptime(date_str, format or "%Y-%m-%dT%H:%M:%S")
    return date


def calculate_flight_speed(distance: float, departure_time, arrival_time):
    arrival_time = convert_str_to_datetime(arrival_time)
    departure_time = convert_str_to_datetime(departure_time)
    # Calculate the time in hours
    time_diff_hours = (arrival_time - departure_time).seconds / 3600

    # Calculate speed in km/h
    speed = distance / time_diff_hours
    return speed
