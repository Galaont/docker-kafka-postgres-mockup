-- Create the measurements table with real_timestamp field
CREATE TABLE IF NOT EXISTS measurements (
    id SERIAL PRIMARY KEY,
    temp FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    date_time TIMESTAMP NOT NULL,
    real_timestamp TIMESTAMP NOT NULL
);

-- Create the temperature report table
CREATE TABLE IF NOT EXISTS temperature_report (
    id SERIAL PRIMARY KEY,
    avg_temp FLOAT NOT NULL,
    measurement_start_time TIMESTAMP NOT NULL,
    measurement_end_time TIMESTAMP NOT NULL,
    real_start_time TIMESTAMP NOT NULL,
    real_end_time TIMESTAMP NOT NULL
);

-- Create the humidity report table
CREATE TABLE IF NOT EXISTS humidity_report (
    id SERIAL PRIMARY KEY,
    avg_humidity FLOAT NOT NULL,
    measurement_start_time TIMESTAMP NOT NULL,
    measurement_end_time TIMESTAMP NOT NULL,
    real_start_time TIMESTAMP NOT NULL,
    real_end_time TIMESTAMP NOT NULL
);
