import time
import datetime
import pandas as pd
from sqlalchemy import create_engine, text

DB_PARAMS = {
    "host": "postgres",
    "port": "5432",
    "database": "sensor_data",
    "user": "postgres_user",
    "password": "postgres_password"
}

CONN_STR = f"postgresql+psycopg2://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['database']}"

def table_exists(engine, table_name):
    """Check if a table exists in the database."""
    query = text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = :table_name
        )
    """)
    with engine.connect() as conn:
        return conn.execute(query, {"table_name": table_name}).scalar()

def get_latest_timestamps(engine):
    """Get the latest timestamps from the report tables."""
    last_temp_time = last_humidity_time = None
    with engine.connect() as conn:
        if table_exists(engine, "temperature_report"):
            result = conn.execute(text("SELECT MAX(real_end_time) FROM temperature_report"))
            last_temp_time = result.scalar()
        
        if table_exists(engine, "humidity_report"):
            result = conn.execute(text("SELECT MAX(real_end_time) FROM humidity_report"))
            last_humidity_time = result.scalar()
    
    return last_temp_time, last_humidity_time

def get_oldest_timestamp(engine):
    """Get the oldest timestamp in the measurements table."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT MIN(real_timestamp) FROM measurements"))
        return result.scalar()

def process_temperature_data(engine, last_temp_time):
    """Process temperature data for the last 10-minute interval."""
    with engine.connect() as conn:
        oldest_time = get_oldest_timestamp(engine) or datetime.datetime.now()
    
    start_time = last_temp_time or oldest_time
    end_time = start_time + datetime.timedelta(minutes=10)
    
    query = text('''
        SELECT AVG(temp) as avg_temp
        FROM measurements
        WHERE real_timestamp >= :start_time AND real_timestamp < :end_time
    ''')
    
    df = pd.read_sql(query, engine, params={"start_time": start_time, "end_time": end_time})

    if not df.empty and df.iloc[0]['avg_temp'] is not None:
        with engine.begin() as conn:
            conn.execute(text('''
                INSERT INTO temperature_report (avg_temp, measurement_start_time, measurement_end_time, real_start_time, real_end_time)
                VALUES (:avg_temp, :start_time, :end_time, :start_time, :end_time)
            '''), {
                "avg_temp": df.iloc[0]['avg_temp'],
                "start_time": start_time,
                "end_time": end_time
            })

def process_humidity_data(engine, last_humidity_time):
    """Process humidity data for the last 20-minute interval."""
    with engine.connect() as conn:
        oldest_time = get_oldest_timestamp(engine) or datetime.datetime.now()
    
    start_time = last_humidity_time or oldest_time
    end_time = start_time + datetime.timedelta(minutes=20)
    
    query = text('''
        SELECT AVG(humidity) as avg_humidity
        FROM measurements
        WHERE real_timestamp >= :start_time AND real_timestamp < :end_time
    ''')
    
    df = pd.read_sql(query, engine, params={"start_time": start_time, "end_time": end_time})

    if not df.empty and df.iloc[0]['avg_humidity'] is not None:
        with engine.begin() as conn:
            conn.execute(text('''
                INSERT INTO humidity_report (avg_humidity, measurement_start_time, measurement_end_time, real_start_time, real_end_time)
                VALUES (:avg_humidity, :start_time, :end_time, :start_time, :end_time)
            '''), {
                "avg_humidity": df.iloc[0]['avg_humidity'],
                "start_time": start_time,
                "end_time": end_time
            })

def main():
    engine = create_engine(CONN_STR)
    while True:
        last_temp_time, last_humidity_time = get_latest_timestamps(engine)
        process_temperature_data(engine, last_temp_time)
        process_humidity_data(engine, last_humidity_time)
        time.sleep(600)  # Run every 10 minutes

if __name__ == "__main__":
    main()
