#!/bin/bash

# Setup venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
fi

# Install dependencies (backend specific)
./venv/bin/pip install -r requirements.txt

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

# Kill any existing process on port 8002
fuser -k 8000/tcp 2>/dev/null || true
sleep 1

# Run Uvicorn (using port 8002 to avoid conflicts)
echo "Starting FastAPI Server on port 8000..."
./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
