import pandas as pd
from kafka import KafkaProducer
import json
import time
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor-data")

# Load Parquet data
df = pd.read_parquet("measurements.parquet")
df["date_time"] = pd.to_datetime(df["date_time"])

start_time = df["date_time"].min()
real_start = datetime.now()

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Send messages at real-time intervals
for _, row in df.iterrows():
    event_time = row["date_time"]
    elapsed = (event_time - start_time).total_seconds()
    target_time = real_start + pd.to_timedelta(elapsed, unit="s")
    
    while datetime.now() < target_time:
        time.sleep(0.1)  # Small delay to stay in sync

    message = {
        "id": row["id"],
        "temp": row["temp"],
        "humidity": row["humidity"],
        "measurement_timestamp": row["date_time"].isoformat(),
        "real_timestamp": datetime.now().isoformat(),  # Real timestamp of sending
    }
    producer.send(KAFKA_TOPIC, value=message)
    logging.info(f"Sent: {message}")

producer.flush()
producer.close()
