#!/usr/bin/env bash
set -o errexit  # Exit on error

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "✅ Starting Gunicorn..."
gunicorn dcrm.wsgi:application --bind 0.0.0.0:10000

