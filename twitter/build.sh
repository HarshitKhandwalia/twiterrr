#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting simple build process..."
echo "Current directory: $(pwd)"

echo "Installing basic requirements..."
pip install -r ../requirements.txt

echo "Creating media directory..."
mkdir -p media

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!" 