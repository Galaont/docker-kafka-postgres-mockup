# Use a specific Python image version as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the consumer script
CMD ["python", "consumer.py"]
