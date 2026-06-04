#!/usr/bin/env bash
set -euo pipefail

MAX_ATTEMPTS="${MAX_ATTEMPTS:-3}"
attempt=1

while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
  echo "== Verification attempt ${attempt}/${MAX_ATTEMPTS} =="
  if bash scripts/run_local_ci.sh; then
    echo "Verification passed."
    exit 0
  fi
  attempt=$((attempt + 1))
  echo "Verification failed; retrying after a short pause."
  sleep 2
done

echo "Verification did not pass after ${MAX_ATTEMPTS} attempts." >&2
exit 1
