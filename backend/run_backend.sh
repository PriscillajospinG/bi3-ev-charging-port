#!/bin/bash

# Setup venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
fi

# Install dependencies (backend specific)
./venv/bin/pip install -r requirements.txt

# Load environment variables
# Load environment variables
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Run Uvicorn
# We run from current dir so "app.main" resolves correctly
echo "Starting FastAPI Server..."
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
