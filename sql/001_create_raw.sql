CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.race_results (
    season        INT,
    round         INT,
    race_name     TEXT,
    race_date     DATE,
    driver_id     TEXT,
    driver_name   TEXT,
    constructor   TEXT,
    grid          INT,
    position      INT,
    points        NUMERIC,
    status        TEXT,
    PRIMARY KEY (season, round, driver_id)
);