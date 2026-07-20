#!/bin/bash

set -e

echo "[INFO] Running migrations..."
python manage.py make_migrations
python manage.py migrate
echo "[INFO] Database migrations completed successfully."

