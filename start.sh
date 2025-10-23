#!/usr/bin/env bash
# Exit on error
set -o errexit  

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "✅ Starting Gunicorn..."
gunicorn dcrm.wsgi:application --bind 0.0.0.0:8000
