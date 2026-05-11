#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Importing questions..."
python manage.py import_questions

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"
