#!/bin/bash
set -e

echo "=== Didacta Backend Startup ==="

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Run database seed
echo "Running database seed..."
python manage.py seed_db

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8001 backend.wsgi:application
