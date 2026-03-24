-- routes
CREATE TABLE IF NOT EXISTS routes (
    route_id         SERIAL PRIMARY KEY,
    origin_iata      VARCHAR(3)  NOT NULL,
    destination_iata VARCHAR(3)  NOT NULL,
    is_active        BOOLEAN     NOT NULL DEFAULT TRUE,
    UNIQUE (origin_iata, destination_iata)
);

-- search_configs
CREATE TABLE IF NOT EXISTS search_configs (
    search_id      SERIAL PRIMARY KEY,
    route_id       INTEGER     NOT NULL REFERENCES routes(route_id),
    departure_date DATE        NOT NULL,
    adults         INTEGER     NOT NULL,
    cabin          VARCHAR(20) NOT NULL,
    currency       VARCHAR(3)  NOT NULL,
    non_stop       BOOLEAN     NOT NULL DEFAULT FALSE
);

-- fare_snapshots
CREATE TABLE IF NOT EXISTS fare_snapshots (
    snapshot_id             BIGSERIAL PRIMARY KEY,
    search_id               INTEGER       NOT NULL REFERENCES search_configs(search_id),
    carrier_code            VARCHAR(8),
    validating_airline_code VARCHAR(8),
    departure_time          TIMESTAMP,
    arrival_time            TIMESTAMP,
    stops                   INTEGER,
    duration_minutes        INTEGER,
    price_total             NUMERIC(12,2),
    currency                VARCHAR(3),
    collected_at            TIMESTAMP     NOT NULL
);

-- pipeline_runs
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id          BIGSERIAL PRIMARY KEY,
    started_at      TIMESTAMP   NOT NULL,
    finished_at     TIMESTAMP,
    status          VARCHAR(20) NOT NULL,
    rows_inserted   INTEGER     DEFAULT 0,
    error_message   TEXT
);