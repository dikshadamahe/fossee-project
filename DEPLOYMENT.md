# Deployment Guide

This guide covers deploying the FOSSEE Chemical Equipment Parameter Visualizer to production.

---

## 🌐 Web Frontend (Vercel)

### Prerequisites
- GitHub account
- Vercel account (free tier works)

### Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `web-frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Set Environment Variables**
   In Vercel dashboard → Settings → Environment Variables:
   ```
   VITE_API_URL = https://your-username.pythonanywhere.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy automatically

### Custom Domain (Optional)
- Settings → Domains → Add your custom domain

---

## 🐍 Backend (PythonAnywhere)

### Prerequisites
- PythonAnywhere account (free tier works for testing)

### Steps

1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Sign up for a free account

2. **Upload Code**
   
   **Option A: Git Clone** (Recommended)
   ```bash
   # In PythonAnywhere Bash console:
   git clone https://github.com/YOUR_USERNAME/fossee-project.git
   cd fossee-project/backend
   ```
   
   **Option B: Upload Files**
   - Use Files tab to upload the `backend` folder

3. **Set Up Virtual Environment**
   ```bash
   cd ~/fossee-project/backend
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

5. **Configure Web App**
   - Go to Web tab → Add a new web app
   - Choose "Manual configuration" → Python 3.12
   - Set:
     - **Source code**: `/home/YOUR_USERNAME/fossee-project/backend`
     - **Virtualenv**: `/home/YOUR_USERNAME/fossee-project/backend/venv`

6. **Edit WSGI Configuration**
   Click on the WSGI configuration file link and replace with:
   ```python
   import os
   import sys
   
   # Add your project directory
   path = '/home/YOUR_USERNAME/fossee-project/backend'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
   os.environ['DJANGO_SECRET_KEY'] = 'your-production-secret-key-here'
   os.environ['DJANGO_DEBUG'] = 'False'
   os.environ['DJANGO_ALLOWED_HOSTS'] = 'YOUR_USERNAME.pythonanywhere.com'
   os.environ['CORS_ALLOWED_ORIGINS'] = 'https://your-vercel-app.vercel.app'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

7. **Reload Web App**
   - Click the green "Reload" button

### Verify Deployment
- Visit `https://YOUR_USERNAME.pythonanywhere.com/api/datasets/`
- Should return empty list or your datasets

---

## 💻 Desktop App (GitHub Releases)

### Build Executable

1. **Run Build Script**
   ```cmd
   cd desktop-app
   build_desktop.bat
   ```

2. **Test Executable**
   - Check `desktop-app/dist/FOSSEE-ChemViz.exe`
   - Run it to verify it works

### Create GitHub Release

1. **Tag Version**
   ```bash
   git tag -a v1.0.0 -m "Initial release"
   git push origin v1.0.0
   ```

2. **Create Release**
   - Go to GitHub → Releases → "Create a new release"
   - Choose tag `v1.0.0`
   - Title: "FOSSEE Chemical Equipment Visualizer v1.0.0"
   - Description: Release notes
   - Attach `FOSSEE-ChemViz.exe`
   - Click "Publish release"

---

## 🔒 Production Checklist

### Security
- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS (automatic on Vercel/PythonAnywhere)

### CORS Configuration
Update `CORS_ALLOWED_ORIGINS` in Django settings:
```python
CORS_ALLOWED_ORIGINS = [
    'https://your-vercel-app.vercel.app',
]
```

### Database
- For production, consider upgrading to PostgreSQL
- PythonAnywhere free tier uses SQLite

---

## 📋 Environment Variables Summary

### Backend (PythonAnywhere)
| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Production secret key | Random 50+ chars |
| `DJANGO_DEBUG` | Debug mode | `False` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hostnames | `username.pythonanywhere.com` |
| `CORS_ALLOWED_ORIGINS` | CORS whitelist | `https://app.vercel.app` |

### Frontend (Vercel)
| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://username.pythonanywhere.com` |

---

## 🔗 Live URLs

After deployment, update these in README.md:

- **Web App**: `https://your-app.vercel.app`
- **API**: `https://your-username.pythonanywhere.com/api/`
- **Desktop**: GitHub Releases page
