#!/bin/bash
# Harbor verifier entry point. Writes the reward to /logs/verifier/reward.txt.
set -u
cp /tests/test_choice_prefix.py /app/tests/test_choice_prefix.py
python3 /tests/grade.py
