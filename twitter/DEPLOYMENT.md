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

⚠️ **CRITICAL**: Do NOT use `python manage.py runserver` as the start command!

### 4. Environment Variables (Set in Render Dashboard)
- `SECRET_KEY`: Generate a new secret key (IMPORTANT: Don't use the default one!)
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Set to `twiterrr.onrender.com,localhost,127.0.0.1`
- `RENDER`: Set to `true` (tells Django it's running on Render)

**⚠️ CRITICAL**: Generate a new SECRET_KEY! The default one in settings.py is not secure for production.

### 5. Configure Persistent Disk for Media Files
**IMPORTANT**: Set this up BEFORE your first deployment to avoid losing uploaded files!

1. **In the Render Dashboard**, go to your Web Service
2. **Navigate to "Disks"** in the left sidebar
3. **Click "Add Disk"**:
   - **Name**: `media-storage` (or any name you prefer)
   - **Mount Path**: `/opt/render/project/src/media`
   - **Size**: Start with 1GB (you can expand later)
4. **Save the disk configuration**

This persistent disk will store all uploaded media files (images, PDFs, etc.) and persist across deployments and restarts.

### 6. Database
- Render will automatically provide a `DATABASE_URL` environment variable
- The app will use PostgreSQL on Render and SQLite locally

### 7. Deploy
- Click "Create Web Service"
- Render will build and deploy your app automatically

## File Structure
```
DjangoTwitter/
├── requirements.txt          # Production requirements (for Render)
├── twitter/                 # Source directory (set in Render)
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
- **Media files are stored on a persistent disk** and won't be lost during deployments
- The app automatically switches between SQLite (local) and PostgreSQL (Render)
- Media files are served by Django in production (suitable for hobby projects)
- No Docker required - Render handles the containerization

## Troubleshooting

### Common Issues:
1. **400 Bad Request Error**: Usually caused by ALLOWED_HOSTS or SECRET_KEY issues
2. **Static files error**: Ensure the `static/` directory exists and contains files
3. **Auth context processor error**: Fixed in settings.py
4. **Port binding**: Use `$PORT` environment variable in start command
5. **Build failures**: Check the build logs for specific error messages

### If you get 400 errors:
1. **Check SECRET_KEY**: Must be a new, secure key (not the default)
2. **Check ALLOWED_HOSTS**: Must include your Render domain
3. **Check DEBUG**: Must be set to False in production
4. **Check environment variables**: All must be set correctly in Render

### Environment Variables Checklist:
- ✅ `SECRET_KEY`: New, secure key (generate one!)
- ✅ `DEBUG`: `False`
- ✅ `ALLOWED_HOSTS`: `twiterrr.onrender.com,localhost,127.0.0.1`
- ✅ `RENDER`: `true` (enables persistent disk media storage)
- ✅ `DATABASE_URL`: Automatically provided by Render

### Media Files Troubleshooting:
1. **Uploaded files disappear after deployment**: Ensure persistent disk is configured with mount path `/opt/render/project/src/media`
2. **Can't access uploaded images**: Check that `RENDER=true` environment variable is set
3. **Media files not displaying**: Verify the persistent disk is properly mounted and has sufficient storage