import requests


class MockAirlineAPIConnector:
    def __init__(self) -> None:
        self.apikey = "pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc"
        self.username = "demo"
        self.password = "swnvlD"

    def get_flights(self, origin: str, destination: str, departure_date: str) -> dict:
        endpoint = f"https://stub.amopromo.com/air/search/{self.apikey}/{origin}/{destination}/{departure_date}"
        response = requests.get(endpoint, auth=(self.username, self.password))
        response.raise_for_status()
        return response.json()
