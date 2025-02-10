import logging
import json
import os
import psycopg2
from kafka import KafkaConsumer
from psycopg2.extras import RealDictCursor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configurations
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor-data")

# PostgreSQL configurations
PG_HOST = os.getenv("PG_HOST", "postgres")
PG_PORT = os.getenv("PG_PORT", 5432)
PG_DB = os.getenv("PG_DB", "sensor_data")
PG_USER = os.getenv("POSTGRES_USER", "user")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")

# Connect to PostgreSQL
def get_pg_connection():
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise

# Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id="sensor-group",  # Consumer group
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest"  # Ensure it starts from the earliest message if no offset exists
)

# Process messages and insert into PostgreSQL
def process_and_store_message(message):
    try:
        # Access the message values
        temperature = message.get('temp')
        humidity = message.get('humidity')
        measurement_timestamp = message.get('measurement_timestamp')
        real_timestamp = message.get('real_timestamp')  # Real timestamp for logging

        # Establish PostgreSQL connection
        conn = get_pg_connection()
        cursor = conn.cursor()

        # Insert data into the measurements table
        cursor.execute(
            "INSERT INTO measurements (temp, humidity, date_time, real_timestamp) VALUES (%s, %s, %s, %s)",
            (temperature, humidity, measurement_timestamp, real_timestamp)
        )

        # Commit the transaction
        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"Stored data: {message}")

    except Exception as e:
        logger.error(f"Failed to process message: {e}")

# Consume messages
logger.info(f"Starting consumer for topic: {KAFKA_TOPIC}")
for message in consumer:
    logger.info(f"Received message: {message.value}") 
    process_and_store_message(message.value)
