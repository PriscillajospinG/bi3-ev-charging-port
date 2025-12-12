#!/bin/bash

# Setup virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
fi

# Install dependencies if requirements changed
./venv/bin/pip install -r requirements.txt

# Run the dashboard engine
echo "Running Dashboard Engine..."
./venv/bin/python dashboard_engine.py
