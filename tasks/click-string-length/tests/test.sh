#!/bin/bash
# Harbor verifier entry point. Writes the reward to /logs/verifier/reward.txt.
set -u
# Install click as a package so importlib.metadata can find it; source comes from /app/src.
python3 -m pip install -q -e /app
cp /tests/test_string_length.py /app/tests/test_string_length.py
python3 /tests/grade.py
