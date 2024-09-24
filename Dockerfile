FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    netcat-openbsd && \ 
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Run the collectstatic command
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 customer_orders_service.wsgi:application"]