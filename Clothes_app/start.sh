#!/bin/sh

echo "Running Migrations..."
python manage.py migrate --noinput

echo "Starting Celery Worker..."
celery -A Clothes_app worker --loglevel=info &

echo "Starting Django Server..."
gunicorn Clothes_app.wsgi --bind 0.0.0.0:$PORT --timeout 120