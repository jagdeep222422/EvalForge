#!/bin/bash
# Oracle solution: apply the reference patch to the click checkout in /app.
set -euo pipefail
cd /app
git apply "$(dirname "$0")/solution.patch"
