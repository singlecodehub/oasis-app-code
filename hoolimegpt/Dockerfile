# Use Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    && apt-get clean


# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Copy the .env file
COPY .env .env

COPY pathwell-datawarehouse-cbb46dd7a792.json /app/pathwell-datawarehouse-cbb46dd7a792.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/pathwell-datawarehouse-cbb46dd7a792.json"


# Collect static files
RUN python manage.py collectstatic --no-input
# RUN python manage.py collectstatic --no-input && rm /app/pathwell-datawarehouse-cbb46dd7a792.json


# Expose port
EXPOSE 8080

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "hoolimegpt.wsgi"]