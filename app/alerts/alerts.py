from datetime import datetime, UTC
from app.analytics.metrics import get_cheapest_by_route

THRESHOLDS = {
    "LHR-JFK": 500.00,
    "LHR-DXB": 300.00,
    "MAD-LHR": 150.00,
}


class BaseNotifier:
    def send(self, route: str, price: float, threshold: float, currency: str) -> None:
        raise NotImplementedError


class ConsoleNotifier(BaseNotifier):
    def send(self, route: str, price: float, threshold: float, currency: str) -> None:
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"[{timestamp}] FARE ALERT")
        print(f"  Route:     {route}")
        print(f"  Price:     {currency} {price:.2f}")
        print(f"  Threshold: {currency} {threshold:.2f}")
        print(f"  Status:    BELOW threshold — consider booking")
        print()


def check_alerts(notifiers: list[BaseNotifier] = None) -> None:
    if notifiers is None:
        notifiers = [ConsoleNotifier()]

    df = get_cheapest_by_route()

    if df.empty:
        print("No fare data available. Run the pipeline first.")
        return

    triggered = 0

    for _, row in df.iterrows():
        route_key = f"{row['origin_iata']}-{row['destination_iata']}"
        threshold = THRESHOLDS.get(route_key)

        if threshold is None:
            continue

        price = float(row["cheapest_price"])
        currency = row["currency"]

        if price < threshold:
            for notifier in notifiers:
                notifier.send(route_key, price, threshold, currency)
            triggered += 1

    if triggered == 0:
        print(f"No alerts triggered. Checked {len(df)} route(s) against thresholds.")
    else:
        print(f"{triggered} alert(s) triggered.")


if __name__ == "__main__":
    check_alerts()