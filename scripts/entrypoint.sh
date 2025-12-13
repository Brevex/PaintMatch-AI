#!/bin/bash
set -e

# Configuration
TIMEOUT=60
COUNTER=0

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  COUNTER=$((COUNTER + 1))
  if [ $COUNTER -gt $TIMEOUT ]; then
    echo "ERROR: Failed to connect to PostgreSQL after ${TIMEOUT}s"
    exit 1
  fi
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Creating database tables..."
python scripts/create_tables.py

if [ "$LOAD_SEED_DATA" = "true" ]; then
  echo "Loading seed data..."
  python scripts/load_data.py
fi

echo "Starting application..."
exec "$@"
