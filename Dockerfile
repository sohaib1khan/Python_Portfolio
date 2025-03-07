# Use a lightweight Python base image
FROM python:3.11-slim

# Set environment variables to optimize for container usage
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_APP=app.py

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and assets
COPY app.py ./
COPY content/ ./content/
COPY static/ ./static/
COPY templates/ ./templates/

# Expose the application port
EXPOSE 8989

# Use Gunicorn for production readiness
RUN pip install --no-cache-dir gunicorn

# Run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8989", "app:app"]
