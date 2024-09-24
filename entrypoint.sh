#!/bin/bash
set -e

source venv/bin/activate

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

exec gunicorn --bind 0.0.0.0:8000 customer_orders_service.wsgi:application
