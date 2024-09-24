FROM python:3.8

WORKDIR /app

# Install dependencies, including netcat
RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    netcat && \  
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Create a virtual environment
RUN python3 -m venv venv

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Collect static files
RUN venv/bin/python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]