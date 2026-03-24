"""
Pipeline entry point: fetch -> normalize -> store.

Run with:
    python -m app.pipeline.run_pipeline
"""

from datetime import datetime, UTC
from app.pipeline.fetch_offers import fetch_and_save
from app.pipeline.normalize_offers import normalize_all
from app.db.connection import SessionLocal
from app.db.models import Route, SearchConfig, FareSnapshot, PipelineRun
from app.pipeline.fetch_offers import (
    ORIGIN, DESTINATION, DEPARTURE_DATE,
    ADULTS, TRAVEL_CLASS, CURRENCY_CODE, NON_STOP
)


def get_or_create_route(session, origin: str, destination: str) -> Route:
    route = session.query(Route).filter_by(
        origin_iata=origin, destination_iata=destination
    ).first()
    if not route:
        route = Route(origin_iata=origin, destination_iata=destination)
        session.add(route)
        session.flush()
    return route


def get_or_create_search_config(session, route: Route) -> SearchConfig:
    config = session.query(SearchConfig).filter_by(
        route_id=route.route_id,
        departure_date=DEPARTURE_DATE,
        adults=ADULTS,
        cabin=TRAVEL_CLASS,
        currency=CURRENCY_CODE,
        non_stop=NON_STOP,
    ).first()
    if not config:
        config = SearchConfig(
            route_id=route.route_id,
            departure_date=DEPARTURE_DATE,
            adults=ADULTS,
            cabin=TRAVEL_CLASS,
            currency=CURRENCY_CODE,
            non_stop=NON_STOP,
        )
        session.add(config)
        session.flush()
    return config


def run() -> None:
    started_at = datetime.now(UTC)
    print("=== Flight Fare Monitor Pipeline ===")

    with SessionLocal() as session:
        pipeline_run = PipelineRun(started_at=started_at, status="running")
        session.add(pipeline_run)
        session.flush()

        try:
            raw_offers = fetch_and_save()
            if not raw_offers:
                pipeline_run.status = "no_data"
                pipeline_run.finished_at = datetime.now(UTC)
                session.commit()
                print("No offers fetched. Exiting.")
                return

            rows = normalize_all(raw_offers, collected_at=started_at)
            print(f"Normalized: {len(rows)} rows")

            route = get_or_create_route(session, ORIGIN, DESTINATION)
            config = get_or_create_search_config(session, route)

            snapshots = [
                FareSnapshot(
                    search_id=config.search_id,
                    carrier_code=r["carrier_code"],
                    validating_airline_code=r["validating_airline_code"],
                    departure_time=r["departure_time"],
                    arrival_time=r["arrival_time"],
                    stops=r["stops"],
                    duration_minutes=r["duration_minutes"],
                    price_total=r["price_total"],
                    currency=r["currency"],
                    collected_at=started_at,
                )
                for r in rows
            ]
            session.add_all(snapshots)

            pipeline_run.status = "success"
            pipeline_run.finished_at = datetime.now(UTC)
            pipeline_run.rows_inserted = len(snapshots)
            session.commit()

            print(f"Stored: {len(snapshots)} snapshots")
            print(f"Pipeline run ID: {pipeline_run.run_id}")
            print("Done.")

        except Exception as e:
            pipeline_run.status = "error"
            pipeline_run.finished_at = datetime.now(UTC)
            pipeline_run.error_message = str(e)
            session.commit()
            print(f"Pipeline failed: {e}")
            raise


if __name__ == "__main__":
    run()