# Django Rules - Consolidated Checklists

Référence consolidée de toutes les checklists des guides Django (01-15).

---

## 01. Architecture du Projet

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

---

## 02. Modèles & ORM

### Structure
- [ ] App uses `models/` package with `__init__.py` re-exporting classes
- [ ] One file per main model, `mixins.py` for abstract bases
- [ ] No circular imports between model files

### Fields
- [ ] PascalCase class names, snake_case field names
- [ ] `max_length` explicit on all CharField
- [ ] `DecimalField` for money (not FloatField)
- [ ] `verbose_name` and `help_text` on non-trivial fields

### Relations
- [ ] `on_delete` explicit: PROTECT for refs, SET_NULL/CASCADE for secondary
- [ ] `related_name` defined on all FK/M2M
- [ ] Intermediate model for M2M when audit/metadata needed

### Constraints & Performance
- [ ] `CheckConstraint` for business invariants
- [ ] `UniqueConstraint` for uniqueness rules
- [ ] `db_index=True` or `Meta.indexes` on filtered columns
- [ ] Custom QuerySet with `select_related`/`prefetch_related` for common patterns

### Behavior
- [ ] Abstract mixins for timestamps, soft-delete, audit
- [ ] No heavy business logic in `save()`, `clean()`, or signals
- [ ] No network calls or ETL in models

### Migrations
- [ ] No modification of committed migrations
- [ ] No large ETL in migrations (use commands)
- [ ] Schema and data migrations separated

---

## 03. Couche Services

### Structure
- [ ] App has `services/` with `usecases/`, `domain/`, `integrations/` as needed
- [ ] Shared technical services in `shared/services/`
- [ ] DTOs defined in `dto.py` using `@dataclass`
- [ ] Business exceptions in `exceptions.py`

### Use Cases
- [ ] Non-trivial business operations are in `services/usecases/`
- [ ] Views/ViewSets/Commands contain NO business logic
- [ ] Use cases wrapped in `transaction.atomic()` when needed

### Domain Services
- [ ] Pure business rules in `services/domain/` - no I/O
- [ ] Models stay thin (no 2000-line god models)

### Integrations
- [ ] ALL external calls (HTTP, files, ERP) go through `services/integrations/`
- [ ] Use cases never do direct `requests.get()` or file I/O

### Security & Errors
- [ ] Use cases accept `user` parameter for authorization
- [ ] Authorization logic in `permissions.py`
- [ ] Business exceptions properly defined and raised

### Signals
- [ ] Signals only for lightweight side-effects (logging, metrics, notifications)
- [ ] Main business logic NEVER in signals

### ETL
- [ ] ETL structured as `extract_*/transform_*/load_*` in `services/etl/`
- [ ] Large imports use `bulk_create`/`bulk_update`
- [ ] ETL operations are idempotent when possible

### Tests
- [ ] Each critical service has tests in `tests/test_services_*.py`
- [ ] External integrations are mocked in tests

---

## 04. Vues & URLs

### URL Structure
- [ ] `config/urls.py` only includes app URLs via `include()` - no logic
- [ ] Each app has `urls.py` with `app_name` defined
- [ ] URLs are namespaced (`namespace="taxe_sejour"`)
- [ ] Routes have names (`name="detail"`, `name="liste"`)
- [ ] Consistent naming: `liste`, `detail`, `creer`, `modifier`, `supprimer`
- [ ] Path converters used consistently (`uuid` for sensitive, `int` for refs)

### Views Organization
- [ ] Views in `views/backoffice.py`, `views/public.py`, `views/exports.py`
- [ ] CRUD uses generic CBVs (ListView, DetailView, CreateView, etc.)
- [ ] FBV only for simple cases (healthcheck, redirects)

### Views Behavior
- [ ] NO business logic in views - delegate to services
- [ ] `LoginRequiredMixin` on all sensitive views
- [ ] `PermissionRequiredMixin` where needed
- [ ] `get_queryset()` uses `select_related`/`prefetch_related`
- [ ] Lists have `paginate_by`

### Service Integration
- [ ] Use cases called from views, not inline logic
- [ ] `request.user` passed to services for security/audit
- [ ] Transactions managed in services, not views
- [ ] Service exceptions caught and converted to user messages

### Navigation
- [ ] No hardcoded URLs - always `reverse()` or `{% url %}`
- [ ] Custom error handlers defined (400, 403, 404, 500)

---

## 05. Templates & Frontend

### Template Structure
- [ ] `TEMPLATES` config uses `DIRS` + `APP_DIRS=True`
- [ ] Global templates in `backend/templates/`
- [ ] App templates in `apps/<app>/templates/<app>/`
- [ ] Partials clearly identified (`_` prefix or `partials/` folder)
- [ ] All pages extend a base layout

### Template Quality
- [ ] No direct ORM access in templates
- [ ] Logic limited to control tags only
- [ ] Filters used for presentation formatting
- [ ] URLs generated with `{% url %}` tag

### HTMX
- [ ] HTMX script loaded in base layout
- [ ] `hx-boost="true"` for navigation where appropriate
- [ ] HTMX endpoints return partials (not full pages)
- [ ] Views detect `request.htmx` for response type
- [ ] `hx-target` avoids React zones

### React Islands
- [ ] React roots defined via `<div id="...">` elements
- [ ] Props passed via `data-*` attributes
- [ ] Bundles included via Vite helper
- [ ] React consumes API endpoints (not HTML)
- [ ] React zones not manipulated by HTMX

### i18n & Accessibility
- [ ] `{% trans %}` used for translatable strings
- [ ] `aria-live` regions for HTMX updates
- [ ] Loading indicators for async operations

---

## 06. API DRF

### Architecture & Structure
- [ ] Each app has `api/` module (serializers, viewsets, routers, filters)
- [ ] Routes exposed under `/api/v1/<domain>/`
- [ ] Clear separation: `views/` (HTML) vs `api/` (JSON)

### Serializers
- [ ] No heavy business logic in serializers
- [ ] `ModelSerializer` for CRUD operations
- [ ] `Serializer` for use case DTOs
- [ ] Complex validation delegated to services

### Views & ViewSets
- [ ] `ModelViewSet` / `ReadOnlyModelViewSet` for CRUD
- [ ] Custom actions via `@action` decorator
- [ ] ViewSets remain thin: I/O → services
- [ ] Appropriate HTTP status codes returned

### Permissions & Security
- [ ] `DEFAULT_AUTHENTICATION_CLASSES` configured
- [ ] `DEFAULT_PERMISSION_CLASSES` = `[IsAuthenticated]`
- [ ] Domain permissions wrapped in DRF classes
- [ ] Public endpoints explicitly documented and limited

### Filtering & Pagination
- [ ] Pagination enabled with reasonable `PAGE_SIZE`
- [ ] Filters via `DjangoFilterBackend`
- [ ] `ordering_fields` explicitly whitelisted
- [ ] Indexes exist for filtered/sorted columns

### Service Integration
- [ ] No direct complex ORM in ViewSets
- [ ] All business logic in `services/`
- [ ] Heavy ETL uses async jobs (not HTTP thread)

---

## 07. Formulaires & Validation

### Organization & Structure
- [ ] Each app has `forms/` directory with context-based files
- [ ] `forms/` contains only form logic (no services, no ETL)
- [ ] Shared forms in `shared/forms/` if needed (rare)

### Form Types
- [ ] Simple CRUD → `ModelForm`
- [ ] Use case specific → `Form` + service
- [ ] `ModelForm.save()` not overloaded with business logic

### Validation
- [ ] Simple field validation in `clean_<field>()`
- [ ] Cross-field validation in `clean()`
- [ ] Structural invariants in models + DB constraints
- [ ] Business rules in services
- [ ] `is_valid()` always called before using `cleaned_data`

### Security & UX
- [ ] All POST forms include `{% csrf_token %}`
- [ ] No `|safe` on uncontrolled user data
- [ ] Clear error messages (field-specific vs non-field)

### Multiple Items & Files
- [ ] Formsets used only when UX requires multiple objects
- [ ] File uploads use `FileField` + ETL service for processing
- [ ] `enctype="multipart/form-data"` on upload forms

---

## 08. Settings & Environnements

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

---

## 09. Sécurité & Conformité

### Configuration & Deployment
- [ ] `DEBUG = False` in production
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] `SECRET_KEY` from environment, not in Git
- [ ] Secure cookies enabled (SESSION/CSRF)
- [ ] HSTS configured with appropriate duration
- [ ] `python manage.py check --deploy` passes
- [ ] `check --deploy` integrated in CI/CD pipeline

### Authentication & Sessions
- [ ] Django auth for backoffice
- [ ] DRF auth configured (Session and/or JWT)
- [ ] `DEFAULT_PERMISSION_CLASSES = [IsAuthenticated]`
- [ ] Password validators configured
- [ ] Login throttling implemented

### Authorization
- [ ] Domain permissions centralized in `apps/<app>/permissions.py`
- [ ] Permissions reused in DRF via wrapper classes
- [ ] Object-level permissions for multi-tenant data
- [ ] Queryset filtering by user scope

### Input/Output Protection
- [ ] All POST forms include `{% csrf_token %}`
- [ ] No `|safe` on user-controlled data
- [ ] ORM used for all queries (no raw SQL concatenation)
- [ ] CORS strictly configured (no wildcards)

### Data & Compliance
- [ ] Sensitive data identified and documented
- [ ] Secrets stored in environment/secrets manager
- [ ] Data retention policy defined
- [ ] Anonymization capability for GDPR if needed

### Logging & Monitoring
- [ ] Security events logged (login, permission denied)
- [ ] Audit trail for sensitive operations
- [ ] Log format suitable for aggregation (JSON)
- [ ] Dependencies monitored for vulnerabilities

---

## 10. ETL, Tâches Async & Planification

### Architecture & Organization
- [ ] Each domain with ETL has `services/etl/` module
- [ ] Celery tasks in `tasks/` call pure ETL services
- [ ] Management commands in `management/commands/` for CLI access

### Technology Choices
- [ ] Celery + Redis for async tasks
- [ ] django-celery-beat for periodic scheduling (or simple cron)
- [ ] Single scheduling solution (no mixing)

### Robustness & Idempotency
- [ ] ETL services are idempotent (safe to replay)
- [ ] Tasks use `acks_late`, retries, timeouts
- [ ] Errors logged with context and stack trace

### Security & Governance
- [ ] ETL trigger endpoints require authentication + permissions
- [ ] Destructive commands require `--force` flag
- [ ] ETL executions journaled (who, what, when, result)

### Infrastructure & CI
- [ ] `worker` and `beat` services in Docker stack
- [ ] CI tests ETL services (unit + integration)
- [ ] Monitoring for job success/failure/duration

---

## 11. Tests & Qualité Logicielle

### Organization
- [ ] Each app has `tests/` with `test_models.py`, `test_services.py`, `test_api.py`
- [ ] Business services and ETL have dedicated tests
- [ ] Fixtures/factories in `conftest.py` and `factories.py`

### Backend Tests
- [ ] `pytest` + `pytest-django` used
- [ ] `APIClient` for DRF endpoint tests
- [ ] Forms tested on validation rules
- [ ] Management commands tested (at least happy path)

### Async & ETL
- [ ] Celery tasks tested as thin wrappers
- [ ] ETL services tested with sample files
- [ ] Idempotency tested (run twice, no duplicates)

### Quality
- [ ] Lint (ruff) and format (black) in CI
- [ ] Coverage measured with minimum threshold
- [ ] `manage.py check` and `check --deploy` run regularly

---

## 12. Performance & Scalabilité

### ORM & Database
- [ ] List views use `select_related`/`prefetch_related`
- [ ] Filtered/ordered fields have indexes
- [ ] No Python loops with `obj.related.all()` on large sets

### API & DRF
- [ ] All lists paginated (reasonable size, e.g., 50)
- [ ] `ordering_fields` explicitly whitelisted
- [ ] Serializers don't compute per-object (use annotations)

### Cache
- [ ] Redis configured in production
- [ ] Reference data cached (parameters, configs)
- [ ] Cache invalidation implemented where needed

### ETL & Async
- [ ] Large files processed in chunks
- [ ] Bulk operations used (bulk_create, bulk_update)
- [ ] Heavy work offloaded to Celery

### Scalability
- [ ] Application is stateless
- [ ] Multiple web/worker instances supported
- [ ] Celery queues separated by priority/type

### Monitoring
- [ ] Response time metrics collected
- [ ] Slow query logging enabled
- [ ] Celery queue lengths monitored

---

## 13. Logging & Observabilité

### LOGGING Configuration
- [ ] `LOGGING` defined in dedicated module
- [ ] Console handler with rich formatter
- [ ] Domain-specific loggers configured
- [ ] LOG_LEVEL configurable via environment

### Application Logging
- [ ] ETL services log start/end with volumes
- [ ] API errors logged via custom handler
- [ ] Celery tasks log start/complete/error
- [ ] Security events logged (login, access)

### Audit & Security
- [ ] Sensitive actions journaled
- [ ] No sensitive data in logs
- [ ] Request correlation (request_id) implemented

### Observability
- [ ] Error tracking (Sentry) integrated
- [ ] Metrics collected (response time, errors)
- [ ] Log aggregation configured (ELK/Loki)

### Infrastructure
- [ ] Logs written to stdout/stderr
- [ ] JSON format in production
- [ ] Log retention policy defined

---

## 14. CI/CD & Déploiement

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

---

## 15. Conventions de Code

### Quick Reference for AI Agents

```yaml
Stack: Django 5, DRF, PostgreSQL, Celery, Redis, pytest

Structure:
  - apps/<app>/models/
  - apps/<app>/services/{usecases,domain,etl}/
  - apps/<app>/api/{serializers,viewsets,routers}.py
  - apps/<app>/tasks/
  - apps/<app>/tests/

Conventions:
  - snake_case: functions, variables
  - PascalCase: classes
  - Services: pure logic, return dataclasses
  - Tasks: thin wrappers calling services
  - DRF: IsAuthenticated by default
  - Tests: pytest, one tests/ per app

Tools:
  - ruff: linting
  - black: formatting
  - pytest: testing
  - coverage: code coverage
```

### Where to Create New Code

| Type | Location |
|------|----------|
| Model | `apps/<app>/models/<model>.py` |
| Service (use case) | `apps/<app>/services/usecases/<action>.py` |
| ETL Service | `apps/<app>/services/etl/<job>.py` |
| API Serializer | `apps/<app>/api/serializers.py` |
| API ViewSet | `apps/<app>/api/viewsets.py` |
| Form | `apps/<app>/forms/<context>_forms.py` |
| Celery Task | `apps/<app>/tasks/<domain>_tasks.py` |
| Management Command | `apps/<app>/management/commands/<name>.py` |
| Test | `apps/<app>/tests/test_<module>.py` |

### Never Create Business Logic In

- `config/` (settings, URLs, WSGI only)
- Serializers (validation only)
- Views/ViewSets (I/O orchestration only)
- Celery tasks (thin wrappers only)
- Templates (presentation only)
