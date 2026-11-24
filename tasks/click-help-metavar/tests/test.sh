#!/bin/bash
# Harbor verifier entry point. Writes the reward to /logs/verifier/reward.txt.
set -u
cp /tests/test_help_metavar.py /app/tests/test_help_metavar.py
python3 /tests/grade.py
