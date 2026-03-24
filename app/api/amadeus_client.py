import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

class AmadeusClient:

    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("AMADEUS_API_KEY and AMADEUS_API_SECRET must be set in your .env file.")

    def get_access_token(self) -> str:
        try:
            response = requests.post(
                TOKEN_URL,
                data={"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.api_secret},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10,
            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Could not reach Amadeus. Check your internet connection.")
        except requests.exceptions.Timeout:
            raise TimeoutError("Amadeus auth request timed out.")
        if response.status_code != 200:
            raise RuntimeError(f"Auth failed ({response.status_code}): {response.text}")
        token = response.json().get("access_token")
        if not token:
            raise RuntimeError("Auth response did not contain an access_token.")
        return token

    def search_flights(self, origin, destination, departure_date, adults=1, travel_class="ECONOMY", currency_code="GBP", non_stop=False, max_offers=10) -> list[dict]:
        token = self.get_access_token()
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": adults,
            "travelClass": travel_class,
            "currencyCode": currency_code,
            "nonStop": str(non_stop).lower(),
            "max": max_offers,
        }
        try:
            response = requests.get(SEARCH_URL, headers={"Authorization": f"Bearer {token}"}, params=params, timeout=15)
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Could not reach Amadeus search API.")
        except requests.exceptions.Timeout:
            raise TimeoutError("Flight search request timed out.")
        if response.status_code != 200:
            raise RuntimeError(f"Search failed ({response.status_code}): {response.text}")
        return response.json().get("data", [])

if __name__ == "__main__":
    try:
        client = AmadeusClient()
        token = client.get_access_token()
        print("Authentication successful.")
        print(f"Token: {token[:20]}...")
    except Exception as e:
        print(f"Error: {e}")
