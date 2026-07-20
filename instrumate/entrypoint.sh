#!/bin/sh

set -e

echo "[INFO] Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "[INFO] Starting server..."
exec "$@"
