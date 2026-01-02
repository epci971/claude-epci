# Django Architecture Reference

## Project Structure

```
backend/
├── config/                         # Project configuration
│   ├── settings/
│   │   ├── base.py                # Shared settings
│   │   ├── dev.py                 # Development (DEBUG=True)
│   │   ├── test.py                # Test runner settings
│   │   └── prod.py                # Production (secure)
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py
├── apps/                          # Business domain applications
│   └── <domain>/
│       ├── models/                # Model package
│       │   ├── __init__.py        # Re-exports
│       │   ├── <entity>.py        # One file per main model
│       │   └── mixins.py          # Abstract base classes
│       ├── services/              # Business logic layer
│       │   ├── usecases/          # Application services
│       │   ├── domain/            # Pure business rules
│       │   ├── integrations/      # External systems
│       │   └── etl/               # Data pipelines
│       ├── api/                   # DRF components
│       │   ├── serializers.py
│       │   ├── viewsets.py
│       │   ├── routers.py
│       │   └── filters.py
│       ├── views/                 # Django views
│       │   ├── backoffice.py
│       │   ├── public.py
│       │   └── exports.py
│       ├── forms/                 # Django forms
│       ├── permissions.py         # Domain permissions
│       ├── tasks/                 # Celery tasks
│       ├── management/commands/   # CLI commands
│       ├── admin.py
│       ├── urls.py                # App URLs with app_name
│       └── tests/
│           ├── test_models.py
│           ├── test_services.py
│           └── test_api.py
├── shared/                        # Cross-app utilities
│   ├── models.py                  # Base models (TimeStampedModel)
│   ├── permissions.py             # Shared permissions
│   └── utils.py
├── templates/                     # Global templates
├── static/                        # Static files
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
└── pyproject.toml
```

## Service Layer Architecture

### Layer Responsibilities

| Layer | Purpose | I/O Allowed |
|-------|---------|-------------|
| `usecases/` | Application orchestration | Yes (DB, services) |
| `domain/` | Pure business rules | **No** (pure functions) |
| `integrations/` | External systems | Yes (APIs, files) |
| `etl/` | Data pipelines | Yes (bulk operations) |

### Use Case Pattern

```python
# apps/production/services/usecases/cloturer_campagne.py
from dataclasses import dataclass
from django.db import transaction
from apps.production.models import Campagne, Bilan
from apps.production.services.domain import calculer_bilan

@dataclass
class CloturerCampagneResult:
    campagne: Campagne
    bilan: Bilan

@transaction.atomic
def cloturer_campagne(campagne_id: int, user) -> CloturerCampagneResult:
    """
    Use case: Close a campaign and generate final report.

    Args:
        campagne_id: Campaign to close
        user: User performing the action (for authorization)

    Returns:
        CloturerCampagneResult with updated campaign and generated bilan

    Raises:
        PermissionDenied: If user lacks permission
        ValidationError: If campaign cannot be closed
    """
    campagne = Campagne.objects.select_for_update().get(id=campagne_id)

    # Authorization check
    if not user.has_perm('production.cloturer_campagne', campagne):
        raise PermissionDenied()

    # Delegate to domain service (pure business logic)
    bilan_data = calculer_bilan(campagne)

    # Persist changes
    campagne.status = 'TERMINE'
    campagne.save()

    bilan = Bilan.objects.create(campagne=campagne, **bilan_data)

    return CloturerCampagneResult(campagne=campagne, bilan=bilan)
```

### Domain Service Pattern

```python
# apps/production/services/domain/calculs.py
from decimal import Decimal
from typing import Dict, Any

def calculer_bilan(campagne) -> Dict[str, Any]:
    """
    Pure business logic - no database access.

    Takes data, returns computed result.
    Easy to test, no mocking needed.
    """
    total_quantite = sum(lot.quantite for lot in campagne.lots.all())
    taux_conformite = _calculer_taux_conformite(campagne.lots.all())

    return {
        'quantite_totale': total_quantite,
        'taux_conformite': taux_conformite,
        'note': _generer_note(taux_conformite),
    }

def _calculer_taux_conformite(lots) -> Decimal:
    """Helper: compute conformity rate."""
    if not lots:
        return Decimal('0')
    conformes = sum(1 for lot in lots if lot.est_conforme)
    return Decimal(conformes) / Decimal(len(lots)) * 100
```

### Integration Service Pattern

```python
# apps/production/services/integrations/erp_client.py
import httpx
from django.conf import settings
from typing import Optional

class ERPClient:
    """External ERP system integration."""

    def __init__(self):
        self.base_url = settings.ERP_API_URL
        self.timeout = 30

    def get_article(self, code: str) -> Optional[dict]:
        """Fetch article from ERP."""
        try:
            response = httpx.get(
                f"{self.base_url}/articles/{code}",
                headers=self._get_headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"ERP error: {e}", extra={'code': code})
            return None

    def _get_headers(self) -> dict:
        return {'Authorization': f'Bearer {settings.ERP_API_TOKEN}'}
```

## URL Configuration

### Root URLs (config/urls.py)

```python
# config/urls.py - Only aggregation, no logic
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/v1/', include('apps.production.api.urls')),
    path('api/v1/', include('apps.qualite.api.urls')),

    # Web routes
    path('production/', include('apps.production.urls', namespace='production')),
    path('qualite/', include('apps.qualite.urls', namespace='qualite')),
]
```

### App URLs

```python
# apps/production/urls.py
from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('campagnes/', views.CampagneListView.as_view(), name='campagne-liste'),
    path('campagnes/<int:pk>/', views.CampagneDetailView.as_view(), name='campagne-detail'),
    path('campagnes/creer/', views.CampagneCreateView.as_view(), name='campagne-creer'),
    path('campagnes/<int:pk>/modifier/', views.CampagneUpdateView.as_view(), name='campagne-modifier'),
]
```

## Settings by Environment

### base.py (Shared)

```python
# config/settings/base.py
import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read .env file
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'rest_framework',
    'django_filters',
    # Apps
    'apps.production',
    'apps.qualite',
]

DATABASES = {
    'default': env.db('DATABASE_URL')
}

# DRF Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}
```

### dev.py

```python
# config/settings/dev.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Debug toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Relaxed security for development
CORS_ALLOW_ALL_ORIGINS = True
```

### prod.py

```python
# config/settings/prod.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'DENY'

# Caching
CACHES = {
    'default': env.cache('REDIS_URL')
}
```

## Views Pattern

### Thin Views (Delegate to Services)

```python
# apps/production/views/backoffice.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.shortcuts import redirect

from apps.production.models import Campagne
from apps.production.forms import CampagneForm
from apps.production.services.usecases import cloturer_campagne

class CampagneListView(LoginRequiredMixin, ListView):
    model = Campagne
    template_name = 'production/campagne_list.html'
    paginate_by = 25

    def get_queryset(self):
        return Campagne.objects.select_related('responsable')\
                               .prefetch_related('lots')\
                               .order_by('-created_at')

class CampagneClotureView(PermissionRequiredMixin, View):
    permission_required = 'production.cloturer_campagne'

    def post(self, request, pk):
        try:
            result = cloturer_campagne(campagne_id=pk, user=request.user)
            messages.success(request, f"Campagne clôturée. Bilan: {result.bilan.id}")
        except ValidationError as e:
            messages.error(request, str(e))

        return redirect('production:campagne-detail', pk=pk)
```
