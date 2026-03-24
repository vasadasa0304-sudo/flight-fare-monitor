CREATE TABLE IF NOT EXISTS fare_snapshots (
    id             SERIAL PRIMARY KEY,
    origin         CHAR(3)        NOT NULL,
    destination    CHAR(3)        NOT NULL,
    departure_date DATE           NOT NULL,
    airline        VARCHAR(10),
    cabin          VARCHAR(20),
    price          NUMERIC(10, 2) NOT NULL,
    currency       CHAR(3)        NOT NULL,
    fetched_at     TIMESTAMPTZ    NOT NULL DEFAULT NOW()
);
