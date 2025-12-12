# Django ETL, Async Tasks & Scheduling Rules

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Interfaces                                             │
│  ├── Backoffice (upload, manual trigger)                │
│  └── API (async job requests)                           │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Services Layer                                         │
│  └── services/etl/ (pure business logic, reusable)      │
└─────────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │                    │                    │
┌────────┴────────┐  ┌───────┴───────┐  ┌────────┴────────┐
│  Celery Tasks   │  │  Management   │  │  Views/API      │
│  (thin wrapper) │  │  Commands     │  │  (trigger)      │
└─────────────────┘  └───────────────┘  └─────────────────┘
         ▲
         │
┌─────────────────────────────────────────────────────────┐
│  Scheduler                                              │
│  ├── Celery Beat (django-celery-beat)                   │
│  └── Cron (simple jobs only)                            │
└─────────────────────────────────────────────────────────┘
```

## Directory Structure

```
apps/
  <app_name>/
    services/
      etl/
        __init__.py
        import_file.py          # ETL service (pure logic)
        export_report.py
        aggregate_daily.py
    tasks/
      __init__.py
      etl_tasks.py              # Celery task wrappers
    management/
      commands/
        import_daily.py         # CLI command
        rebuild_aggregates.py

shared/
  services/
    etl/
      utils.py                  # Common ETL utilities
      journal.py                # ETL logging helpers
```

## ETL Service Pattern

### Pure ETL Service (Reusable)
```python
# apps/labo/services/etl/import_file.py
import logging
from dataclasses import dataclass
from pathlib import Path
from django.db import transaction

logger = logging.getLogger("apps.labo.etl")

@dataclass
class ImportResult:
    rows_read: int
    rows_imported: int
    errors: int
    messages: list[str]

def import_labo_file(path: Path, user_id: int | None = None) -> ImportResult:
    """
    Pure ETL service - no knowledge of Celery, Cron, or HTTP.
    Can be called from: views, tasks, management commands.
    """
    logger.info("Import started", extra={"path": str(path), "user_id": user_id})
    
    rows_read = 0
    rows_imported = 0
    errors = 0
    messages = []
    
    with transaction.atomic():
        # 1. Read source (CSV, XLSX, API, etc.)
        # 2. Validate and transform
        # 3. Upsert to database (idempotent)
        # 4. Log progress
        pass
    
    result = ImportResult(rows_read, rows_imported, errors, messages)
    
    logger.info(
        "Import completed",
        extra={
            "path": str(path),
            "rows_read": result.rows_read,
            "rows_imported": result.rows_imported,
            "errors": result.errors,
        },
    )
    
    return result
```

## Celery Tasks (Thin Wrappers)

### Task Definition
```python
# apps/labo/tasks/etl_tasks.py
import logging
from celery import shared_task
from apps.labo.services.etl.import_file import import_labo_file

logger = logging.getLogger("apps.labo.etl")

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
)
def import_labo_file_task(self, path_str: str, user_id: int | None = None):
    """Thin wrapper - delegates to service."""
    try:
        from pathlib import Path
        result = import_labo_file(Path(path_str), user_id)
        return {
            "rows_imported": result.rows_imported,
            "errors": result.errors,
        }
    except Exception as exc:
        logger.error(
            "Task failed",
            extra={"path": path_str, "user_id": user_id},
            exc_info=True,
        )
        raise self.retry(exc=exc)
```

### Triggering from API
```python
# apps/labo/api/viewsets.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.labo.tasks.etl_tasks import import_labo_file_task

class LaboImportViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ImportInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Async execution - return immediately
        task = import_labo_file_task.delay(
            path_str=serializer.validated_data["file_path"],
            user_id=request.user.id,
        )
        
        return Response(
            {"task_id": task.id, "status": "queued"},
            status=status.HTTP_202_ACCEPTED,
        )
```

## Management Commands

```python
# apps/labo/management/commands/import_daily.py
from django.core.management.base import BaseCommand
from apps.labo.services.etl.import_file import import_labo_file

class Command(BaseCommand):
    help = "Daily labo import from configured source"
    
    def add_arguments(self, parser):
        parser.add_argument("--source", type=str, required=True)
        parser.add_argument("--force", action="store_true")
    
    def handle(self, *args, **options):
        if not options["force"]:
            self.stdout.write("Use --force to confirm execution")
            return
        
        from pathlib import Path
        result = import_labo_file(Path(options["source"]))
        
        self.stdout.write(
            f"Imported {result.rows_imported} rows, {result.errors} errors"
        )
```

## Celery Configuration

### Settings
```python
# config/settings/base.py
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/1")

CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "UTC"
```

### Celery App
```python
# config/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

app = Celery("gardel")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

## Periodic Tasks (Celery Beat)

### Using django-celery-beat
```python
# Admin UI or fixtures to create:
# PeriodicTask: name="Daily Labo Import"
#   task="apps.labo.tasks.etl_tasks.import_labo_file_task"
#   crontab: minute=0, hour=2  (2:00 AM)
#   args='["/data/labo/daily.csv"]'
```

### Alternative: Cron + Management Command
```bash
# crontab
0 2 * * * cd /srv/app && python manage.py import_daily --source=/data/daily.csv --force
```

## Docker Stack

```yaml
# docker-compose.yml
services:
  web:
    image: app-backend:latest
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    
  worker:
    image: app-backend:latest
    command: celery -A config worker -l info -Q default,etl
    
  beat:
    image: app-backend:latest
    command: celery -A config beat -l info
    
  redis:
    image: redis:7-alpine
```

## Idempotency Pattern

```python
# Ensure ETL can be safely re-run
def import_records(records: list[dict]) -> ImportResult:
    for record in records:
        # Use natural key for upsert
        obj, created = Record.objects.update_or_create(
            external_id=record["id"],  # Natural key
            defaults={
                "name": record["name"],
                "value": record["value"],
                "updated_at": timezone.now(),
            },
        )
```

---

## ✅ DO

- ✅ Keep ETL logic in `services/etl/` - pure, testable, reusable
- ✅ Make Celery tasks thin wrappers that call services
- ✅ Return structured results from ETL services (`@dataclass`)
- ✅ Use `acks_late=True` for critical tasks (prevent loss on crash)
- ✅ Implement idempotency (safe to re-run)
- ✅ Log ETL start/end with volumes and status
- ✅ Use Redis as broker (not Django DB)
- ✅ Protect API endpoints that trigger ETL with permissions
- ✅ Use `--force` flag for destructive management commands
- ✅ Separate queues for different task types

---

## ❌ DON'T

- ❌ **No business logic in Celery tasks** - delegate to services
- ❌ **No Django DB as Celery broker** - use Redis/RabbitMQ
- ❌ **No synchronous heavy processing in HTTP thread**
- ❌ **No mixing multiple scheduling solutions** - pick one
- ❌ **No ETL without idempotency** - must be safe to replay
- ❌ **No unprotected ETL endpoints** - require authentication
- ❌ **No secrets in task arguments** - pass IDs, fetch in task
- ❌ **No ETL without logging** - always trace execution

---

## Checklist

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
