# Deployment Guide for Render

## Prerequisites
- GitHub repository with your Django project
- Render account

## Steps to Deploy

### 1. Push your code to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Create a new Web Service on Render
- Go to [render.com](https://render.com)
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Choose the repository

### 3. Configure the Web Service
- **Name**: Choose a name for your app
- **Environment**: Python 3
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn twitter.wsgi:application --bind 0.0.0.0:$PORT`

### 4. Environment Variables (Set in Render Dashboard)
- `SECRET_KEY`: Generate a new secret key
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Set to `your-app-name.onrender.com,localhost,127.0.0.1`

### 5. Database
- Render will automatically provide a `DATABASE_URL` environment variable
- The app will use PostgreSQL on Render and SQLite locally

### 6. Deploy
- Click "Create Web Service"
- Render will build and deploy your app automatically

## File Structure
```
DjangoTwitter/
├── requirements.txt          # Production requirements (for Render)
├── twitter/
│   ├── requirements.txt     # Local development requirements
│   ├── build.sh            # Build script for Render
│   ├── static/             # Static files directory
│   └── manage.py           # Django management
```

## Local Development
- Use `twitter/requirements.txt` for local development
- Copy `twitter/env.example` to `twitter/.env`
- Set `DEBUG=True` for local development
- Run `python manage.py runserver` from the `twitter/` directory

## Important Notes
- Static files are automatically collected during build
- Media files are handled by whitenoise
- The app automatically switches between SQLite (local) and PostgreSQL (Render)
- No Docker required - Render handles the containerization
- The build script automatically finds the correct requirements.txt file

## Troubleshooting

### Common Issues:
1. **Static files error**: Ensure the `static/` directory exists and contains files
2. **Auth context processor error**: Fixed in settings.py
3. **Port binding**: Use `$PORT` environment variable in start command
4. **Build failures**: Check the build logs for specific error messages

### If you see "No open ports detected":
- Make sure your start command uses `$PORT` environment variable
- The app should bind to `0.0.0.0:$PORT` 