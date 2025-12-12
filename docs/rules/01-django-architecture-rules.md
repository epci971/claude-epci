# Django Project Architecture Rules

## Repository Structure

```
project/
├── backend/
│   ├── manage.py
│   ├── pyproject.toml
│   └── src/
│       ├── config/          # Project configuration
│       ├── apps/            # Business domain apps
│       └── shared/          # Cross-cutting utilities
├── frontend/                # React/Vite app
├── infra/
│   └── docker/              # Dockerfiles, docker-compose, nginx
├── docs/                    # Documentation
└── .github/workflows/       # CI/CD pipelines
```

## Backend Structure

```
backend/src/
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          # Common settings
│   │   ├── dev.py           # DEBUG=True, local DB
│   │   ├── test.py          # CI/test settings
│   │   └── prod.py          # DEBUG=False, secrets from env
│   ├── urls.py              # Root URL composition only
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── labo/
│   ├── production/
│   ├── taxe_sejour/
│   └── ...
└── shared/
    ├── models/base.py       # TimeStamped, SoftDelete mixins
    ├── services/            # mailer, pdf, excel
    └── utils/               # dates, math, query helpers
```

## App Internal Structure

Each business app follows this expanded pattern:

```
apps/<domain>/
├── __init__.py
├── apps.py
├── models/
│   ├── __init__.py          # Re-export all models
│   ├── <model_name>.py      # One file per model
│   └── mixins.py
├── services/
│   ├── __init__.py
│   ├── <usecase>.py
│   └── etl_<name>.py
├── api/
│   ├── serializers/<name>.py
│   ├── viewsets/<name>.py
│   └── routers.py
├── views/
│   ├── __init__.py
│   ├── backoffice.py
│   └── public.py
├── urls.py
├── forms/<name>.py
├── admin.py
├── templates/<domain>/
├── static/<domain>/
├── management/commands/     # Django CLI commands
└── tests/
    ├── test_models.py
    ├── test_services.py
    ├── test_api.py
    └── test_views.py
```

## URL Routing Pattern

Root `config/urls.py` only composes app routes:

```python
# config/urls.py
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes under /api/
    path("api/taxe/", include("apps.taxe_sejour.api.routers")),
    path("api/labo/", include("apps.labo.api.routers")),
    # HTML routes
    path("taxe/", include("apps.taxe_sejour.urls")),
    path("labo/", include("apps.labo.urls")),
]
```

## DO ✅

### App Organization
- One app per business domain (labo, production, taxe_sejour)
- Apps should be potentially reusable (cohesive, self-contained)
- Models as package: `models/` directory with `__init__.py` re-exporting classes
- Separate `api/` (DRF) from `views/` (Django HTML views)
- Tests organized by type: `test_models.py`, `test_services.py`, `test_api.py`

### Settings
- Split settings: `base.py` → `dev.py` / `test.py` / `prod.py`
- Load secrets from environment variables in prod
- Use `django-environ` or similar for env parsing

### Shared Module
- Only truly cross-cutting code: mixins, utils, infrastructure services
- Technical toolbox, NOT business logic

### ETL & Commands
- Management commands in `apps/<domain>/management/commands/`
- ETL logic in `apps/<domain>/services/etl_*.py`
- Commands call services, don't contain business logic

## DON'T ❌

```python
# ❌ Generic catch-all app
apps/
  core/           # BAD - becomes a dumping ground
  common/         # BAD - heterogeneous business logic

# ❌ Business logic in shared/
shared/
  services/
    calcul_taxe.py   # BAD - belongs in apps/taxe_sejour/services/

# ❌ Secrets in code
SECRET_KEY = "hardcoded-secret"  # BAD - use env vars

# ❌ Logic in root urls.py
# config/urls.py
def my_view(request):  # BAD - put in app views
    ...
urlpatterns = [path("x/", my_view)]  # BAD

# ❌ Single monolithic models.py for complex apps
apps/taxe_sejour/
  models.py  # BAD if >200 lines - split into models/ package

# ❌ Mixed API and HTML in same views file
apps/taxe_sejour/
  views.py  # BAD - split into views/ + api/
```

## Checklist

### Repository
- [ ] Repo structured as `backend/`, `frontend/`, `infra/`, `docs/`
- [ ] Backend under `backend/src/` with `config/`, `apps/`, `shared/`
- [ ] CI/CD workflows in `.github/workflows/` or equivalent
- [ ] Docker configs in `infra/docker/`

### Configuration
- [ ] Settings split into `base.py`, `dev.py`, `test.py`, `prod.py`
- [ ] No secrets hardcoded (SECRET_KEY, DB passwords, API tokens)
- [ ] Logging config in `config/logging.py` or `settings/base.py`

### Apps
- [ ] Each business domain = dedicated app in `apps/`
- [ ] App follows expanded pattern: `models/`, `services/`, `api/`, `views/`, `tests/`
- [ ] `INSTALLED_APPS` contains only business apps and third-party libs
- [ ] No catch-all `core` or `common` app with mixed business logic

### Routing
- [ ] Root `config/urls.py` only aggregates app URLs via `include()`
- [ ] Clear separation: `/api/*` for DRF, other paths for Django views
- [ ] Each app has its own `urls.py` and `api/routers.py`

### Shared Module
- [ ] `shared/` contains only cross-cutting utilities (mixins, helpers, infra)
- [ ] No domain-specific business logic in `shared/`
