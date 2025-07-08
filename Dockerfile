# Multi-stage build for production deployment on Render
FROM node:18-alpine AS frontend-builder

# Set work directory for frontend
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci --only=production --legacy-peer-deps

# Copy frontend source code
COPY frontend/ .

# Build frontend for production
RUN npm run build

# Python backend stage
FROM python:3.11-slim AS backend-builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory for backend
WORKDIR /app/backend

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy backend source code
COPY backend/ .

# Final production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=prtcltech.settings

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        nginx \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy Python dependencies from backend stage
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend application
COPY --from=backend-builder /app/backend /app/backend

# Copy built frontend from frontend stage
COPY --from=frontend-builder /app/frontend/build /app/static

# Create nginx configuration
RUN echo 'server { \
    listen 80; \
    server_name _; \
    \
    # Serve static files (React build) \
    location / { \
        root /app/static; \
        try_files $uri $uri/ /index.html; \
    } \
    \
    # Proxy API requests to Django \
    location /api/ { \
        proxy_pass http://127.0.0.1:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
    \
    # Proxy admin and other Django URLs \
    location /admin/ { \
        proxy_pass http://127.0.0.1:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
}' > /etc/nginx/sites-available/default

# Create startup script
RUN echo '#!/bin/bash \n\
# Start Django with Gunicorn in background \n\
cd /app/backend \n\
python manage.py migrate --noinput \n\
python manage.py collectstatic --noinput \n\
gunicorn prtcltech.wsgi:application --bind 127.0.0.1:8000 --workers 3 --timeout 120 & \n\
\n\
# Start nginx in foreground \n\
nginx -g "daemon off;"' > /app/start.sh

RUN chmod +x /app/start.sh

# Expose port
EXPOSE 80

# Start the application
CMD ["/app/start.sh"] 