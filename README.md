## To-Do List:
- [x] **Get docker compose template running**
      Define a single `docker-compose.yml` that includes all required services: Kafka (provided), PostgreSQL, and containers for the sensor data producer, consumer, and batch processor (ETL).
- [x] **Streaming Component – Sensor Data Producer**
    - Create a script to read the `measurements.parquet` file.
	- Process each record one by one, differentiating between Temperature and Humidity measurements.
	- Write each record as a message to the appropriate Kafka topic.
- [x] **Consumer Component**
    - Develop a service that consumes messages from the Kafka instance.
	- Write the consumed data into your chosen database (ensure it’s declared in your Docker Compose).
- [x] **Batch Processing (ETL) Component**
    - Read data from the database populated by the consumer.
    - Compute the average temperature over 10-minute intervals and the average humidity over 20-minute intervals.
    - Write the resulting summaries into the PostgreSQL instance.
- [ ] **Testing & Documentation**
    - Write unit tests for each component (streaming, consumer, ETL).
    - Create an architectural drawing of your solution and save it in a folder named `solution-files`.
- [ ] **Final Packaging**
    - Ensure all code, tests, Docker Compose configuration, and documentation are included.
    - Zip the project files for submission.