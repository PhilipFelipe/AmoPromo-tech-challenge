import os
from dotenv import load_dotenv
import requests

load_dotenv()

class MockAirlineAPIConnector:
    def __init__(self) -> None:
        self.username: str = os.getenv("USERNAME", "")
        self.password: str = os.getenv("PASSWORD", "")
        self.api_key: str = os.getenv("API_KEY", "")

    def get_flights(self, origin: str, destination: str, departure_date: str) -> dict:
        endpoint = f"https://stub.amopromo.com/air/search/{self.apikey}/{origin}/{destination}/{departure_date}"
        response = requests.get(endpoint, auth=(self.username, self.password))
        response.raise_for_status()
        return response.json()
