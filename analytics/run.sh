#!/bin/bash

# Ensure libomp is found for XGBoost on macOS
if command -v brew &> /dev/null; then
    export LIBOMP_PATH=$(brew --prefix libomp)/lib
    export DYLD_LIBRARY_PATH=$LIBOMP_PATH:$DYLD_LIBRARY_PATH
fi

# Run the engine
./venv/bin/python demand_prediction_engine.py
