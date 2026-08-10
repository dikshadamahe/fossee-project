"""
Django settings for Chemical Equipment Parameter Visualizer
FOSSEE Scientific Analytics UI
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings - use environment variables in production
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-fossee-chemical-equipment-visualizer-change-in-production'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Allowed hosts - extend for production
_default_hosts = 'localhost,127.0.0.1,fossee-project-api.vercel.app'
_allowed_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', _default_hosts)
ALLOWED_HOSTS = [host.strip() for host in _allowed_hosts.split(',') if host.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'rest_framework',
    'rest_framework.authtoken',  # Token authentication
    'corsheaders',
    # Local apps
    'equipment',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Vercel serverless has ephemeral filesystem; use /tmp for SQLite
if os.environ.get('VERCEL'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Vercel serverless filesystem is read-only except /tmp
if os.environ.get('VERCEL'):
    MEDIA_ROOT = Path('/tmp/media')
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CORS Configuration
# =============================================================================
_default_cors_origins = (
    'http://localhost:3000,'
    'http://127.0.0.1:3000,'
    'http://localhost:5173,'
    'http://127.0.0.1:5173,'
    'https://fossee-project.vercel.app,'
    'https://fossee-project-eta.vercel.app,'
    'https://fossee-project-api.vercel.app'
)
_cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', _default_cors_origins)
CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in _cors_origins.split(',') if origin.strip()
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# CSRF Trusted Origins (for Django 4.0+)
CSRF_TRUSTED_ORIGINS = [
    'https://fossee-project.vercel.app',
    'https://fossee-project-eta.vercel.app',
    'https://fossee-project-api.vercel.app',
]

# =============================================================================
# REST Framework Configuration
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.LenientTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Individual views set permissions
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# =============================================================================
# Application Settings
# =============================================================================
MAX_DATASETS = 5  # Max datasets per user (or globally for anonymous)

# Max upload size: 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Production security
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
