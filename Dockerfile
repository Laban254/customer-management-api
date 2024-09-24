FROM python:3.8

WORKDIR /app
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    netcat-openbsd && \ 
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python3 -m venv venv

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

RUN venv/bin/python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "venv/bin/python manage.py migrate && venv/bin/gunicorn --bind 0.0.0.0:8000 customer_orders_service.wsgi:application"]