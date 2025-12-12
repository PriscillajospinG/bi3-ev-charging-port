FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (libomp for xgboost, build-essential for others)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app /app/app
# Copy the models data for seeding (as requested)
COPY models /app/models

# Command to run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
