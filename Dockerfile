FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and models
COPY src/ src/
COPY models/ models/
# Copy data if needed for unique crops list (or better, save unique crops to a json)
COPY data/processed/merged_data.csv data/processed/merged_data.csv

# Expose API port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
