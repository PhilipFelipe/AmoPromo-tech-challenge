from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()


class DomesticAirportAPIConnector:
    def __init__(self):
        self.username: str = os.getenv("USERNAME", "")
        self.password: str = os.getenv("PASSWORD", "")
        self.api_key: str = os.getenv("API_KEY", "")

    def retrieve_airports(self) -> dict:
        url = f"https://stub.amopromo.com/air/airports/{self.api_key}"
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        response.raise_for_status()
        return response.json()
