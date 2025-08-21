#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Listing files:"
ls -la

# Find the project root (where requirements.txt is located)
if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt in current directory"
    PROJECT_ROOT="."
elif [ -f "twitter/requirements.txt" ]; then
    echo "Found requirements.txt in twitter/ subdirectory"
    PROJECT_ROOT="twitter"
else
    echo "ERROR: Could not find requirements.txt"
    exit 1
fi

echo "Installing production requirements from $PROJECT_ROOT/requirements.txt..."
pip install -r "$PROJECT_ROOT/requirements.txt"

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!" 