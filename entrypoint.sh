#!/bin/bash
set -e

while ! nc -z db 5432; do   
  echo "Waiting for the database..."
  sleep 2
done

source venv/bin/activate

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

exec gunicorn --bind 0.0.0.0:8000 customer_orders_service.wsgi:application
