import requests
from requests.auth import HTTPBasicAuth


class DomesticAirportAPIConnector:
    def __init__(self):
        self.username: str = "demo"
        self.password: str = "swnvlD"
        self.api_key: str = "pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc"

    def retrieve_airports(self) -> dict:
        url = f"https://stub.amopromo.com/air/airports/{self.api_key}"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        response.raise_for_status()
        return response.json()
