
import json

from datetime import datetime, UTC

from pathlib import Path

from app.api.amadeus_client import AmadeusClient

# --- Sample search parameters — edit these to test different routes ---

ORIGIN = "LHR"

DESTINATION = "JFK"

DEPARTURE_DATE = "2026-06-01"

ADULTS = 1

TRAVEL_CLASS = "ECONOMY"

CURRENCY_CODE = "GBP"

NON_STOP = False

MAX_OFFERS = 10

# ---------------------------------------------------------------------

RAW_DATA_DIR = Path("data/raw")

def fetch_and_save() -> list[dict]:

    client = AmadeusClient()

    print(f"Searching {ORIGIN} -> {DESTINATION} on {DEPARTURE_DATE}...")

    offers = client.search_flights(

        origin=ORIGIN, destination=DESTINATION, departure_date=DEPARTURE_DATE,

        adults=ADULTS, travel_class=TRAVEL_CLASS, currency_code=CURRENCY_CODE,

        non_stop=NON_STOP, max_offers=MAX_OFFERS,

    )

    if not offers:

        print("No offers returned. The route or date may have no availability in test mode.")

        return []

    timestamp = timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

    filename = RAW_DATA_DIR / f"{ORIGIN}_{DESTINATION}_{DEPARTURE_DATE}_{timestamp}.json"

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(filename, "w") as f:

        json.dump(offers, f, indent=2)

    print(f"Offers returned: {len(offers)}")

    print(f"Raw response saved: {filename}")

    return offers

if __name__ == "__main__":

    try:

        fetch_and_save()

    except Exception as e:

        print(f"Error: {e}")

