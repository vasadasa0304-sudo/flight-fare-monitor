CREATE INDEX IF NOT EXISTS idx_snapshots_search_id
    ON fare_snapshots (search_id);

CREATE INDEX IF NOT EXISTS idx_snapshots_collected_at
    ON fare_snapshots (collected_at DESC);

CREATE INDEX IF NOT EXISTS idx_snapshots_search_collected
    ON fare_snapshots (search_id, collected_at DESC);

CREATE INDEX IF NOT EXISTS idx_search_configs_route_id
    ON search_configs (route_id);

CREATE INDEX IF NOT EXISTS idx_search_configs_departure_date
    ON search_configs (departure_date);

CREATE INDEX IF NOT EXISTS idx_routes_is_active
    ON routes (is_active)
    WHERE is_active = TRUE;
