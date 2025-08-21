# Deployment Guide for Railway

## Prerequisites
- GitHub repository with your Django project
- Railway account

## Steps to Deploy

### 1. Push your code to GitHub
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Create a new Project on Railway
- Go to [railway.app](https://railway.app)
- Click "New Project" → "Deploy from GitHub repo"
- Connect your GitHub repository
- Choose the repository

### 3. Configure the Service
- Railway will auto-detect Python and Django
- **Root Directory**: Set to `twitter/` (where manage.py is located)
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command**: `gunicorn twitter.wsgi:application --bind 0.0.0.0:$PORT`

⚠️ **CRITICAL**: Make sure the root directory points to the `twitter/` folder where `manage.py` is located!

### 4. Environment Variables (Set in Railway Dashboard)
- `SECRET_KEY`: Generate a new secret key (IMPORTANT: Don't use the default one!)
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Set to `your-app-name.up.railway.app,localhost,127.0.0.1`
- `RAILWAY_ENVIRONMENT`: This is automatically set by Railway

**⚠️ CRITICAL**: Generate a new SECRET_KEY! The default one in settings.py is not secure for production.

### 5. Configure Railway Volume for Media Files
**IMPORTANT**: Set this up to persist uploaded files across deployments!

1. **In the Railway Dashboard**, go to your service
2. **Navigate to "Variables"** tab
3. **Add a Volume**:
   - **Mount Path**: `/app/media`
   - **Size**: Railway provides free storage up to your plan limits
4. **Deploy the changes**

This volume will store all uploaded media files (images, PDFs, etc.) and persist across deployments and restarts.

### 6. Database
- Railway can provide a PostgreSQL database (add it as a service)
- The app will use PostgreSQL on Railway and SQLite locally
- Railway will automatically provide a `DATABASE_URL` environment variable

### 7. Configure railway.toml (Optional but Recommended)
A `railway.toml` file has been created in the project root to optimize Railway deployment:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn twitter.wsgi:application --bind 0.0.0.0:$PORT"
restartPolicyType = "on_failure"

[environments.production]
variables = { DEBUG = "False" }
```

### 8. Deploy
- Railway will automatically deploy when you push to your connected branch
- Monitor the build logs in the Railway dashboard

## File Structure
```
DjangoTwitter/
├── requirements.txt          # Root requirements (if needed)
├── twitter/                 # Source directory (set as Root Directory in Railway)
│   ├── requirements.txt     # Main requirements file
│   ├── static/             # Static files directory
│   ├── media/              # Media files (local development)
│   └── manage.py           # Django management
```

## Local Development
- Use `twitter/requirements.txt` for local development
- Copy `twitter/env.example` to `twitter/.env`
- Set `DEBUG=True` for local development
- Run `python manage.py runserver` from the `twitter/` directory

## Important Notes
- Static files are automatically collected during build
- **Media files are stored on Railway Volume** and won't be lost during deployments
- The app automatically switches between SQLite (local) and PostgreSQL (Railway)
- Media files are served by Django in production (suitable for hobby projects)
- Railway handles containerization automatically
- Railway Volumes are included in most plans without extra cost

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
- ✅ `ALLOWED_HOSTS`: `your-app-name.up.railway.app,localhost,127.0.0.1`
- ✅ `RAILWAY_ENVIRONMENT`: Automatically set by Railway
- ✅ `DATABASE_URL`: Automatically provided by Railway (if PostgreSQL service added)

### Media Files Troubleshooting:
1. **Uploaded files disappear after deployment**: Ensure Railway Volume is configured with mount path `/app/media`
2. **Can't access uploaded images**: Check that the volume is properly mounted
3. **Media files not displaying**: Verify the volume has sufficient storage and correct permissions
4. **Build failures**: Ensure Root Directory is set to `twitter/` in Railway settings