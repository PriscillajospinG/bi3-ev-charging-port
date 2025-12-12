#!/bin/bash
if command -v brew &> /dev/null; then
    export LIBOMP_PATH=$(brew --prefix libomp)/lib
    export DYLD_LIBRARY_PATH=$LIBOMP_PATH:$DYLD_LIBRARY_PATH
fi
./venv/bin/python analytics_backend.py
