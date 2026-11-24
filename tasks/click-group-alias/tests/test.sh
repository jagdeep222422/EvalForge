#!/bin/bash
# Harbor verifier entry point. Writes the reward to /logs/verifier/reward.txt.
set -u
cp /tests/test_group_alias.py /app/tests/test_group_alias.py
python3 /tests/grade.py
