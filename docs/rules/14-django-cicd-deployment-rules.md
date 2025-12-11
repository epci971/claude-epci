# Django CI/CD & Deployment Rules

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Static Checks                                 │
│  └── Lint (ruff), Format (black), Security scan         │
├─────────────────────────────────────────────────────────┤
│  Phase 2: Tests                                         │
│  └── pytest, coverage, manage.py check                  │
├─────────────────────────────────────────────────────────┤
│  Phase 3: Build                                         │
│  └── Docker build, tag, push to registry                │
├─────────────────────────────────────────────────────────┤
│  Phase 4: Deploy                                        │
│  └── Pull, migrate, collectstatic, restart              │
└─────────────────────────────────────────────────────────┘
```

## Phase 1: Static Checks

### Commands
```bash
# Linting
ruff check .

# Formatting
black --check .

# Type checking (optional)
mypy apps/ shared/

# Security scan (optional)
pip-audit
# or: safety check
```

## Phase 2: Tests & Checks

### Commands
```bash
# Run tests
pytest --maxfail=3 -q

# Coverage
coverage run -m pytest
coverage report --fail-under=70
coverage xml  # For CI artifact

# Django checks
python manage.py check

# Deployment checks (with prod-like settings)
DJANGO_SETTINGS_MODULE=config.settings.prod \
DJANGO_SECRET_KEY=test-secret \
DJANGO_ALLOWED_HOSTS=localhost \
python manage.py check --deploy
```

### Test Database in CI
```yaml
# GitLab CI / GitHub Actions
services:
  - postgres:16
  - redis:7

variables:
  DATABASE_URL: postgres://postgres:postgres@postgres:5432/test_db
  CELERY_BROKER_URL: redis://redis:6379/0
```

## Phase 3: Docker Build

### Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY src/ ./src/

ENV PYTHONPATH=/app/src
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

# Default command (overridden in compose)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Build & Push
```bash
# Build with commit SHA tag
docker build -t registry.example.com/app-backend:${CI_COMMIT_SHA} backend/

# Push to registry
docker push registry.example.com/app-backend:${CI_COMMIT_SHA}

# Tag as latest (optional)
docker tag registry.example.com/app-backend:${CI_COMMIT_SHA} \
           registry.example.com/app-backend:latest
docker push registry.example.com/app-backend:latest
```

## Phase 4: Deployment

### Docker Compose (Production)
```yaml
# docker-compose.prod.yml
version: "3.9"

services:
  web:
    image: registry.example.com/app-backend:${IMAGE_TAG}
    env_file: .env.prod
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.prod
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz/"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    image: registry.example.com/app-backend:${IMAGE_TAG}
    env_file: .env.prod
    command: celery -A config worker -l info -Q default,etl
    depends_on:
      - db
      - redis

  beat:
    image: registry.example.com/app-backend:${IMAGE_TAG}
    env_file: .env.prod
    command: celery -A config beat -l info
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    env_file: .env.db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

### Deployment Script
```bash
#!/bin/bash
# deploy.sh
set -e

IMAGE_TAG=${1:-latest}
export IMAGE_TAG

echo "Deploying version: $IMAGE_TAG"

# Pull new images
docker compose -f docker-compose.prod.yml pull web worker beat

# Run migrations
docker compose -f docker-compose.prod.yml run --rm web \
    python manage.py migrate --noinput

# Collect static files
docker compose -f docker-compose.prod.yml run --rm web \
    python manage.py collectstatic --noinput

# Restart services (zero-downtime with health checks)
docker compose -f docker-compose.prod.yml up -d web worker beat

# Health check
sleep 10
curl -f http://localhost:8000/healthz/ || exit 1

echo "Deployment complete!"
```

## Health Check Endpoints

```python
# apps/core/views.py
from django.http import JsonResponse
from django.db import connection

def healthz(request):
    """Basic health check."""
    return JsonResponse({"status": "ok"})

def readiness(request):
    """Readiness check with DB connection test."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ready", "db": "ok"})
    except Exception as e:
        return JsonResponse(
            {"status": "not ready", "db": str(e)},
            status=503,
        )
```

```python
# config/urls.py
urlpatterns = [
    path("healthz/", healthz),
    path("readiness/", readiness),
    # ...
]
```

## Environment Strategy

| Branch | Environment | Deploy |
|--------|-------------|--------|
| `feature/*` | - | CI only (lint, test) |
| `develop` | Staging | Auto |
| `main` | Production | Manual approval |

## GitLab CI Example

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  DJANGO_SETTINGS_MODULE: config.settings.test
  DATABASE_URL: postgres://postgres:postgres@postgres:5432/test_db

# Phase 1: Lint
lint:
  stage: lint
  image: python:3.12-slim
  before_script:
    - pip install ruff black
  script:
    - ruff check .
    - black --check .

# Phase 2: Tests
test:
  stage: test
  image: python:3.12-slim
  services:
    - postgres:16
  before_script:
    - pip install -r requirements.txt
    - pip install -r requirements-dev.txt
  script:
    - pytest --maxfail=3 -q
    - coverage run -m pytest
    - coverage report --fail-under=70
    - python manage.py check

# Phase 3: Build
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA backend/
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
    - develop

# Phase 4: Deploy Staging
deploy_staging:
  stage: deploy
  script:
    - ssh deploy@staging "cd /srv/app && ./deploy.sh $CI_COMMIT_SHA"
  environment:
    name: staging
  only:
    - develop

# Phase 4: Deploy Production
deploy_prod:
  stage: deploy
  script:
    - ssh deploy@prod "cd /srv/app && ./deploy.sh $CI_COMMIT_SHA"
  environment:
    name: production
  when: manual
  only:
    - main
```

## GitHub Actions Example

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff black
      - run: ruff check .
      - run: black --check .

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --maxfail=3
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      - run: python manage.py check

  build:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

---

## ✅ DO

- ✅ Run lint (ruff, black) on every push
- ✅ Run tests with coverage threshold
- ✅ Run `manage.py check` and `check --deploy`
- ✅ Tag Docker images with commit SHA
- ✅ Run migrations before restarting services
- ✅ Implement health check endpoints
- ✅ Use manual approval for production deploys
- ✅ Store secrets in CI variables (not in repo)
- ✅ Use .env files (not committed) for local secrets

---

## ❌ DON'T

- ❌ **No secrets in Git** - use CI variables
- ❌ **No deploy without tests passing**
- ❌ **No skipping migrations** before restart
- ❌ **No auto-deploy to production** without approval
- ❌ **No ignoring check --deploy** warnings
- ❌ **No missing health checks** - required for orchestrators

---

## Deployment Checklist

### CI Pipeline
- [ ] Lint (ruff, black) on every push
- [ ] Tests (pytest) with coverage
- [ ] `manage.py check` executed
- [ ] PostgreSQL/Redis available for integration tests

### Docker Build
- [ ] Dockerfile for backend (web/worker/beat)
- [ ] Images tagged with commit SHA
- [ ] Images pushed to private registry

### Deployment
- [ ] `docker-compose.prod.yml` maintained
- [ ] Deploy script handles: pull, migrate, collectstatic, restart
- [ ] Health checks implemented (`/healthz/`, `/readiness/`)
- [ ] Zero-downtime deployment (rolling update)

### Security & Quality
- [ ] Secrets via environment variables only
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` configured
- [ ] Logs sent to stdout, collected by infra
- [ ] Monitoring/alerting configured
