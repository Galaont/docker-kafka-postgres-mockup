# Use a specific Python image version as the base
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY batch_processor.py .
CMD ["python", "batch_processor.py"]
