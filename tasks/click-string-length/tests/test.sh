#!/bin/bash
# Harbor verifier entry point. Writes the reward to /logs/verifier/reward.txt.
set -u
cp /tests/test_string_length.py /app/tests/test_string_length.py
python3 /tests/grade.py
