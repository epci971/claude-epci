# Django Settings & Environments Rules

## Settings Structure

```
backend/
  src/
    config/
      __init__.py
      settings/
        __init__.py
        base.py          # Common settings (all environments)
        dev.py           # Development (DEBUG=True)
        test.py          # Testing/CI
        prod.py          # Production (DEBUG=False, security)
        components/      # (optional) Thematic modules
          database.py
          cache.py
          security.py
          logging.py
          drf.py
      urls.py
      asgi.py
      wsgi.py
```

## Environment Selection

```bash
# Development
export DJANGO_SETTINGS_MODULE="config.settings.dev"

# Testing/CI
export DJANGO_SETTINGS_MODULE="config.settings.test"

# Production
export DJANGO_SETTINGS_MODULE="config.settings.prod"
```

### Docker Compose
```yaml
services:
  backend:
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
```

## Base Settings (base.py)

```python
# config/settings/base.py
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False),
)

# Read .env file only if it exists (dev only)
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)

# Core
DEBUG = env("DEBUG", default=False)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-insecure-key-change-me")

# Apps
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "django_filters",
    "django_htmx",
    # Project apps
    "apps.items",
    "apps.orders",
    "apps.accounts",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

# URLs & WSGI
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Database (via DATABASE_URL)
DATABASES = {
    "default": env.db("DATABASE_URL", default="postgres://localhost/app_db")
}

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets"]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

## Development Settings (dev.py)

```python
# config/settings/dev.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Debug toolbar (optional)
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]

# Email to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Simplified logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
```

## Test Settings (test.py)

```python
# config/settings/test.py
from .base import *

DEBUG = False

# Test database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Faster password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Email to memory
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# In-memory cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
```

## Production Settings (prod.py)

```python
# config/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["app.example.com"])

# Security: HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Security: Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security: HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security: Content
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["https://app.example.com"]
)

# Database
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# Cache (Redis)
CACHES = {
    "default": env.cache("DJANGO_CACHE_URL", default="redis://redis:6379/1")
}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

# Logging (structured JSON for log aggregation)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
```

## DRF Settings

```python
# config/settings/base.py (or components/drf.py)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}
```

## Environment Variables (.env.example)

```bash
# .env.example (committed to Git as template)
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/app_db
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CACHE_URL=redis://localhost:6379/1

# Email
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# External APIs
API_KEY_EXTERNAL=
```

## Docker Integration

### docker-compose.yml
```yaml
services:
  backend:
    build: ./backend
    env_file:
      - .env.prod
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=app_db
      - POSTGRES_USER=app_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## Deployment Checklist Command

```bash
# Run before every production deployment
python manage.py check --deploy --settings=config.settings.prod
```

---

## ✅ DO

- ✅ Split settings: `base.py`, `dev.py`, `test.py`, `prod.py`
- ✅ Use `django-environ` for environment variable parsing
- ✅ Load secrets from environment variables only
- ✅ Set `DJANGO_SETTINGS_MODULE` per environment
- ✅ Enable all security flags in production
- ✅ Use `DATABASE_URL` format for database config
- ✅ Run `manage.py check --deploy` in CI/CD pipeline
- ✅ Keep `.env` files out of Git (`.gitignore`)
- ✅ Provide `.env.example` as template
- ✅ Document all required environment variables

---

## ❌ DON'T

- ❌ **No secrets in Git** - use environment variables
- ❌ **No single monolithic settings.py** - split by environment
- ❌ **No DEBUG=True in production**
- ❌ **No empty ALLOWED_HOSTS in production**
- ❌ **No hardcoded database credentials**
- ❌ **No insecure cookies in production** - use SECURE flags
- ❌ **No HSTS disabled in production** - enable for HTTPS
- ❌ **No skipping check --deploy** - run on every deploy

---

## Security Settings Reference

| Setting | Dev | Prod | Description |
|---------|-----|------|-------------|
| `DEBUG` | True | **False** | Error pages, template debug |
| `ALLOWED_HOSTS` | localhost | **domain list** | Valid host headers |
| `SECRET_KEY` | dev-key | **env var** | Crypto signing |
| `SECURE_SSL_REDIRECT` | False | **True** | Force HTTPS |
| `SESSION_COOKIE_SECURE` | False | **True** | HTTPS-only cookies |
| `CSRF_COOKIE_SECURE` | False | **True** | HTTPS-only CSRF |
| `SECURE_HSTS_SECONDS` | 0 | **31536000** | HSTS duration |
| `X_FRAME_OPTIONS` | - | **DENY** | Clickjacking protection |

---

## Checklist

### Structure & Modularization
- [ ] Settings split: `base.py`, `dev.py`, `test.py`, `prod.py`
- [ ] `DJANGO_SETTINGS_MODULE` set correctly per environment
- [ ] No single monolithic settings file

### Secrets & Environment Variables
- [ ] No secrets committed to Git
- [ ] `.env*` files in `.gitignore`
- [ ] `django-environ` (or similar) used properly
- [ ] `DATABASE_URL`, `CACHE_URL`, email vars from environment

### Environment Distinction
- [ ] `dev.py`: `DEBUG=True`, debug tools enabled
- [ ] `test.py`: In-memory DB, fast hashers, memory cache
- [ ] `prod.py`: `DEBUG=False`, all security settings enabled

### Security (Production)
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_SSL_REDIRECT = True` (if HTTPS)
- [ ] `SECURE_HSTS_SECONDS` configured
- [ ] `python manage.py check --deploy` passes

### Infrastructure & CI/CD
- [ ] Docker/orchestrator provides all env vars
- [ ] CI uses `config.settings.test`
- [ ] Deployment scripts run migrations, collectstatic, check --deploy
