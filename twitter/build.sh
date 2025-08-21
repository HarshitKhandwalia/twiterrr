#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Listing files:"
ls -la

echo "Installing production requirements from ../requirements.txt..."
pip install -r ../requirements.txt

echo "Checking Django version:"
python -c "import django; print(django.get_version())"

echo "Checking database connection:"
python manage.py check --database default

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Checking for any remaining issues:"
python manage.py check

echo "Verifying WSGI module location:"
echo "Current directory: $(pwd)"
echo "Looking for wsgi.py:"
find . -name "wsgi.py" -type f

echo "Build completed successfully!" 