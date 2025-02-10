-- Create the measurements table with real_timestamp field
CREATE TABLE IF NOT EXISTS measurements (
    id SERIAL PRIMARY KEY,
    temp FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    date_time TIMESTAMP NOT NULL, -- field for the measurement timestamp
    real_timestamp TIMESTAMP NOT NULL  -- field for the real timestamp
);

-- Create the temperature report table (average per 10-minute interval)
CREATE TABLE IF NOT EXISTS temperature_report (
    id SERIAL PRIMARY KEY,
    avg_temp FLOAT NOT NULL,
    measurement_start_time TIMESTAMP NOT NULL,  -- Start of the 10-minute interval
    measurement_end_time TIMESTAMP NOT NULL,     -- End of the 10-minute interval
    real_start_time TIMESTAMP NOT NULL,  -- Start of the 10-minute interval
    real_end_time TIMESTAMP NOT NULL     -- End of the 10-minute interval
);

-- Create the humidity report table (average per 20-minute interval)
CREATE TABLE IF NOT EXISTS humidity_report (
    id SERIAL PRIMARY KEY,
    avg_humidity FLOAT NOT NULL,
    measurement_start_time TIMESTAMP NOT NULL,  -- Start of the 20-minute interval
    measurement_end_time TIMESTAMP NOT NULL,     -- End of the 20-minute interval
    real_start_time TIMESTAMP NOT NULL,  -- Start of the 10-minute interval
    real_end_time TIMESTAMP NOT NULL     -- End of the 10-minute interval
);
