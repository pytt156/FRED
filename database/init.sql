CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE
    IF NOT EXISTS telemetry (
        time TIMESTAMPTZ NOT NULL,
        device_id TEXT NOT NULL,
        source TEXT NOT NULL,
        temperature DOUBLE PRECISION,
        humidity DOUBLE PRECISION,
        light INTEGER,
        motion BOOLEAN,
        wifi_connected BOOLEAN,
        rssi INTEGER
    );

SELECT
    create_hypertable ('telemetry', 'time');