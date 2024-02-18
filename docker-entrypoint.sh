#!/bin/sh

set -e

# If arguments are passed to docker, run them instead
if [ ! "$#" -gt 0 ]; then
  PYTHONPATH=/app python app/main.py
fi

exec "$@"
