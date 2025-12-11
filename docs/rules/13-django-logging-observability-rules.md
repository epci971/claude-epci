# Django Logging & Observability Rules

## Observability Pillars

1. **Structured Logs**: Application events, errors, business actions
2. **Metrics**: Response times, throughput, error rates
3. **Traces**: Request correlation across services (optional)

## Log Levels

| Level | Use Case | Example |
|-------|----------|---------|
| `DEBUG` | Dev only, fine-grained | Variable values, query details |
| `INFO` | Normal operations | ETL start/end, user login |
| `WARNING` | Anomalies (handled) | Retry on external service |
| `ERROR` | Failures (blocking) | Unhandled exception |
| `CRITICAL` | System-wide issues | DB unavailable |

## Logging Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Application (Django, Celery)                           │
│  └── Python logging (LOGGING config)                    │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Handlers                                               │
│  ├── Console (stdout) → Docker logs                     │
│  ├── Sentry (errors)                                    │
│  └── File (optional)                                    │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Log Aggregation                                        │
│  └── ELK / Loki / CloudWatch                            │
└─────────────────────────────────────────────────────────┘
```

## LOGGING Configuration

### Base Configuration
```python
# config/settings/components/logging.py
import os

LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    
    "formatters": {
        "verbose": {
            "format": (
                "[{levelname}] {asctime} {name} "
                "request_id={request_id} - {message}"
            ),
            "style": "{",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(levelname)s %(asctime)s %(name)s %(message)s",
        },
    },
    
    "filters": {
        "request_id": {
            "()": "config.logging_filters.RequestIdFilter",
        },
    },
    
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["request_id"],
        },
        "console_json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["request_id"],
        },
    },
    
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
```

### Production Configuration (JSON)
```python
# config/settings/prod.py
LOGGING["root"]["handlers"] = ["console_json"]
LOGGING["loggers"]["apps"]["handlers"] = ["console_json"]
```

## Request ID Correlation

### Filter Implementation
```python
# config/logging_filters.py
import logging
import threading

_request_id = threading.local()

def set_request_id(request_id: str):
    _request_id.value = request_id

def get_request_id() -> str:
    return getattr(_request_id, "value", "-")

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True
```

### Middleware
```python
# config/middleware.py
import uuid
from config.logging_filters import set_request_id

class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        set_request_id(request_id)
        request.request_id = request_id
        
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response
```

## Logger Naming Convention

```python
# apps/orders/services/usecases/create_order.py
import logging

# Convention: apps.<app_name>[.<submodule>]
logger = logging.getLogger("apps.orders.usecases")

def create_order(data: dict, user) -> Order:
    logger.info(
        "Creating order",
        extra={"user_id": user.id, "items_count": len(data["items"])}
    )
    # ...
```

### Domain-Specific Loggers
```python
# ETL
logger = logging.getLogger("apps.labo.etl")

# Security/Audit
logger = logging.getLogger("apps.security")

# API
logger = logging.getLogger("apps.api")
```

## ETL Logging Pattern

```python
# apps/labo/services/etl/import_file.py
import logging

logger = logging.getLogger("apps.labo.etl")

def import_labo_file(path: Path, user_id: int | None = None) -> ImportResult:
    logger.info(
        "ETL started",
        extra={
            "job": "import_labo_file",
            "path": str(path),
            "user_id": user_id,
        }
    )
    
    try:
        # ... processing ...
        
        logger.info(
            "ETL completed",
            extra={
                "job": "import_labo_file",
                "rows_read": result.rows_read,
                "rows_imported": result.rows_imported,
                "errors": result.errors,
                "duration_ms": duration,
            }
        )
        return result
        
    except Exception as e:
        logger.error(
            "ETL failed",
            extra={
                "job": "import_labo_file",
                "path": str(path),
                "error": str(e),
            },
            exc_info=True,
        )
        raise
```

## DRF Exception Logging

```python
# config/drf_exception_handler.py
import logging
from rest_framework.views import exception_handler

logger = logging.getLogger("apps.api")

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    request = context.get("request")
    view = context.get("view")
    
    if response is None or response.status_code >= 500:
        logger.error(
            "API error",
            extra={
                "view": view.__class__.__name__ if view else None,
                "method": request.method if request else None,
                "path": request.path if request else None,
                "status": getattr(response, "status_code", None),
                "exception": exc.__class__.__name__,
            },
            exc_info=True,
        )
    elif response.status_code >= 400:
        logger.warning(
            "API client error",
            extra={
                "view": view.__class__.__name__ if view else None,
                "path": request.path if request else None,
                "status": response.status_code,
            },
        )
    
    return response
```

### Settings
```python
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "config.drf_exception_handler.custom_exception_handler",
}
```

## Celery Task Logging

```python
# apps/orders/tasks/notification_tasks.py
import logging
from celery import shared_task

logger = logging.getLogger("apps.orders.tasks")

@shared_task(bind=True, max_retries=3)
def send_order_notification(self, order_id: int):
    logger.info("Task started", extra={"order_id": order_id})
    
    try:
        # ... send notification ...
        logger.info("Task completed", extra={"order_id": order_id})
        
    except Exception as exc:
        logger.error(
            "Task failed",
            extra={"order_id": order_id, "attempt": self.request.retries},
            exc_info=True,
        )
        raise self.retry(exc=exc, countdown=60)
```

## Security/Audit Logging

```python
# apps/accounts/views.py
import logging

security_logger = logging.getLogger("apps.security")

def login_view(request):
    # ... authentication logic ...
    
    if user:
        security_logger.info(
            "login_success",
            extra={
                "user_id": user.id,
                "email": user.email,
                "ip": get_client_ip(request),
            }
        )
    else:
        security_logger.warning(
            "login_failed",
            extra={
                "username": form.cleaned_data.get("username"),
                "ip": get_client_ip(request),
            }
        )
```

## Audit Trail Model (Optional)

```python
# shared/models/audit.py
class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )
    action = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=50)
    entity_id = models.CharField(max_length=100)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["entity_type", "entity_id"]),
        ]
```

## Sentry Integration

```python
# config/settings/prod.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),
    ],
    traces_sample_rate=0.1,
    send_default_pii=False,
)
```

---

## ✅ DO

- ✅ Use Python logging module (not print)
- ✅ Configure LOGGING in dedicated component file
- ✅ Use structured logging with `extra={}` dict
- ✅ Implement request_id correlation
- ✅ Name loggers by domain: `apps.<app>.<module>`
- ✅ Log ETL start/end with volumes and duration
- ✅ Log errors with `exc_info=True` for stack trace
- ✅ Write logs to stdout (Docker-friendly)
- ✅ Use JSON format in production
- ✅ Integrate error tracking (Sentry) for production

---

## ❌ DON'T

- ❌ **No print() statements** - use logging
- ❌ **No sensitive data in logs** - no passwords, secrets, PII
- ❌ **No DEBUG level in production** - too verbose
- ❌ **No missing context** - always include relevant IDs
- ❌ **No swallowed exceptions** - log then re-raise
- ❌ **No log files in containers** - use stdout

---

## What to Log

| Event | Level | Required Context |
|-------|-------|------------------|
| ETL start | INFO | job name, source, user |
| ETL complete | INFO | job name, rows, duration |
| ETL failure | ERROR | job name, error, stack |
| API error (5xx) | ERROR | view, path, method, stack |
| API error (4xx) | WARNING | view, path, status |
| Login success | INFO | user_id, IP |
| Login failure | WARNING | username, IP |
| Permission denied | WARNING | user_id, resource |
| Parameter change | INFO | user_id, field, old/new |

---

## Checklist

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
