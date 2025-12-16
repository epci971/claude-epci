# Django Production Reference

## Security Checklist

### Django Security Settings

```python
# config/settings/prod.py

# Basic security
DEBUG = False
SECRET_KEY = env('SECRET_KEY')  # From environment, never in code
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# HTTPS enforcement
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security Policy (via django-csp)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
```

### Deploy Check

```bash
# Run before every deployment
python manage.py check --deploy

# Expected output: System check identified no issues
```

### Password Validation

```python
# config/settings/base.py
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

## CORS Configuration

```python
# For APIs consumed by external frontends
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE

# Strict CORS (production)
CORS_ALLOWED_ORIGINS = [
    'https://app.example.com',
    'https://admin.example.com',
]
CORS_ALLOW_CREDENTIALS = True

# Never in production:
# CORS_ALLOW_ALL_ORIGINS = True  # DANGEROUS
```

## Logging Configuration

```python
# config/settings/base.py
import os

LOG_LEVEL = env('LOG_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
        'simple': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json' if not DEBUG else 'simple',
        },
    },

    'loggers': {
        # Django loggers
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },

        # Application loggers
        'apps': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'apps.production.services': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },

    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
```

### Application Logging

```python
# apps/production/services/usecases/cloturer_campagne.py
import logging

logger = logging.getLogger(__name__)

def cloturer_campagne(campagne_id: int, user) -> Result:
    logger.info(
        "Starting campaign closure",
        extra={
            'campagne_id': campagne_id,
            'user_id': user.id,
            'action': 'cloturer_campagne',
        }
    )

    try:
        result = _do_closure(campagne_id, user)

        logger.info(
            "Campaign closed successfully",
            extra={
                'campagne_id': campagne_id,
                'bilan_id': result.bilan.id,
            }
        )
        return result

    except Exception as e:
        logger.exception(
            "Campaign closure failed",
            extra={'campagne_id': campagne_id}
        )
        raise
```

## Celery Configuration

### Settings

```python
# config/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# config/settings/base.py
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'

# Task settings
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TIME_LIMIT = 300  # 5 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 240  # 4 minutes
```

### Task Pattern

```python
# apps/production/tasks/etl.py
from celery import shared_task
from celery.utils.log import get_task_logger

from apps.production.services.etl import import_lots_from_file

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
)
def import_lots_task(self, file_path: str, campagne_id: int):
    """
    Celery task for lot import.

    Thin wrapper around service function.
    """
    logger.info(f"Starting import: {file_path}")

    try:
        count = import_lots_from_file(file_path, campagne_id)
        logger.info(f"Import complete: {count} lots")
        return {'status': 'success', 'count': count}

    except FileNotFoundError as e:
        # Don't retry for missing files
        logger.error(f"File not found: {file_path}")
        return {'status': 'error', 'message': str(e)}

    except Exception as e:
        # Retry for transient errors
        logger.exception("Import failed, retrying")
        raise self.retry(exc=e)
```

## Management Commands

```python
# apps/production/management/commands/import_lots.py
from django.core.management.base import BaseCommand, CommandError
from apps.production.services.etl import import_lots_from_csv

class Command(BaseCommand):
    help = 'Import lots from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to CSV file')
        parser.add_argument('--campagne', type=int, required=True)
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--force', action='store_true',
                           help='Skip confirmation')

    def handle(self, *args, **options):
        filepath = options['filepath']
        campagne_id = options['campagne']

        if not options['force']:
            confirm = input(f"Import from {filepath}? [y/N] ")
            if confirm.lower() != 'y':
                raise CommandError("Import cancelled")

        if options['dry_run']:
            self.stdout.write("DRY RUN - no changes will be made")

        try:
            count = import_lots_from_csv(
                filepath,
                campagne_id,
                dry_run=options['dry_run']
            )
            self.stdout.write(
                self.style.SUCCESS(f'{count} lots imported')
            )
        except Exception as e:
            raise CommandError(f"Import failed: {e}")
```

## Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements/prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: .
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
      - DATABASE_URL
      - REDIS_URL
      - SECRET_KEY
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz/"]
      interval: 30s
      timeout: 10s
      retries: 3

  celery:
    build: .
    command: celery -A config worker -l info
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
      - DATABASE_URL
      - REDIS_URL
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A config beat -l info
    depends_on:
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=myapp
      - POSTGRES_PASSWORD

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## Health Checks

```python
# apps/shared/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Liveness probe."""
    return JsonResponse({'status': 'ok'})

def readiness_check(request):
    """Readiness probe - check dependencies."""
    checks = {}

    # Database
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = str(e)

    # Redis
    try:
        from django.core.cache import cache
        cache.set('health_check', 'ok', 1)
        checks['cache'] = 'ok'
    except Exception as e:
        checks['cache'] = str(e)

    status = 200 if all(v == 'ok' for v in checks.values()) else 503
    return JsonResponse(checks, status=status)
```

## CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  DJANGO_SETTINGS_MODULE: config.settings.test

lint:
  stage: lint
  script:
    - pip install ruff black
    - ruff check apps/
    - black --check apps/

test:
  stage: test
  services:
    - postgres:15
  variables:
    DATABASE_URL: postgres://postgres:postgres@postgres:5432/test
  script:
    - pip install -r requirements/dev.txt
    - pytest --cov=apps --cov-fail-under=70
    - python manage.py check --deploy
  coverage: '/TOTAL.*\s+(\d+%)$/'

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy:
  stage: deploy
  script:
    - docker pull $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker-compose -f docker-compose.prod.yml up -d
    - docker-compose exec web python manage.py migrate --noinput
  environment:
    name: production
  only:
    - main
  when: manual
```

## Production Checklist

| Check | Command/Action | Expected |
|-------|----------------|----------|
| Security check | `manage.py check --deploy` | No issues |
| DEBUG | Settings | `False` |
| SECRET_KEY | Environment | From env var |
| ALLOWED_HOSTS | Settings | Explicit list |
| HTTPS | Settings | `SECURE_SSL_REDIRECT=True` |
| Cookies | Settings | `*_COOKIE_SECURE=True` |
| HSTS | Settings | `SECURE_HSTS_SECONDS > 0` |
| Static files | `collectstatic` | Collected |
| Migrations | `migrate` | Applied |
| Database | Connection | Working |
| Cache | Redis | Connected |
| Celery | Workers | Running |
| Logs | Format | JSON in production |
| Health check | `/healthz/` | Returns 200 |
