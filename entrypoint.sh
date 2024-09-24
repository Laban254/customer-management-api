#!/bin/bash
set -e

# Wait for the database to be available 
while ! nc -z db 5432; do   
  echo "Waiting for the database..."
  sleep 2
done

venv/bin/python manage.py makemigrations
venv/bin/python manage.py migrate

exec venv/bin/gunicorn --bind 0.0.0.0:8000 customer_orders_service.wsgi:application
