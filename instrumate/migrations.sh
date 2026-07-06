#!/bin/bash

# Run migration instructions for the Django application
echo "Starting database migrations..."
python manage.py make_migrations
python manage.py migrate
echo "Database migrations completed successfully."

