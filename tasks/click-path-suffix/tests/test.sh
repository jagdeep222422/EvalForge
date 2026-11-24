#!/bin/bash
# Harbor verifier entry point. Writes the reward to /logs/verifier/reward.txt.
set -u
cp /tests/test_path_suffix.py /app/tests/test_path_suffix.py
python3 /tests/grade.py
