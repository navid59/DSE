FROM python:3.10-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y curl netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements including ray
COPY backend-ray/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 👇 Ensure ray CLI is available globally
RUN pip install ray

# Copy your app
COPY backend-ray/ /app/
WORKDIR /app/

