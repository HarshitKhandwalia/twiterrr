#!/usr/bin/env python
import os
import subprocess
import sys

# Change to the twitter directory where manage.py and wsgi.py are located
os.chdir('twitter')

# Get the port from environment, default to 8000 if not set
port = os.environ.get('PORT', '8000')

# Build the gunicorn command
cmd = [
    'gunicorn',
    'twitter.wsgi:application',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '3',
    '--timeout', '120'
]

print(f"Starting server on port {port}")
print(f"Working directory: {os.getcwd()}")
print(f"Command: {' '.join(cmd)}")

# Execute gunicorn
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error starting server: {e}")
    sys.exit(1)