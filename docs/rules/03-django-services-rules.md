# Django Services Layer Rules

## Architecture Overview

```
Views / ViewSets / Commands  →  Application Services (Use Cases)
                                        ↓
                              Domain Services (Business Rules)
                                        ↓
                              Models & ORM
                                        
Application Services also call:
  - Integration Services (external APIs, files, ERP)
  - Technical Services (mailer, PDF, Excel)
```

**Principle**: Views = thin (I/O glue), Models = structure, Services = business logic

## Services Directory Structure

### Per App

```
apps/<domain>/
├── services/
│   ├── __init__.py
│   ├── usecases/              # Application services (orchestration)
│   │   ├── calculer_taxe.py
│   │   └── generer_rapport.py
│   ├── domain/                # Pure business rules
│   │   └── regles_taxe.py
│   ├── integrations/          # External systems
│   │   ├── erp_bridge.py
│   │   └── geo_provider.py
│   ├── etl/                   # Extract/Transform/Load
│   │   ├── extract_xlsx.py
│   │   ├── transform_data.py
│   │   └── load_data.py
│   ├── dto.py                 # Data Transfer Objects
│   └── transformers.py
├── exceptions.py              # Business exceptions
└── permissions.py             # Authorization policies
```

### Shared Services

```
shared/
├── services/
│   ├── mailer.py              # Email service
│   ├── pdf.py                 # PDF generation
│   ├── excel.py               # Excel/CSV export
│   └── logging.py             # Structured logging
└── utils/
    ├── dates.py
    └── numbers.py
```

## Service Types

### 1. Use Cases (Application Services)

Orchestrate complete business scenarios:

```python
# apps/taxe_sejour/services/usecases/calculer_taxe.py
from dataclasses import dataclass
from django.db import transaction
from ..domain.regles_taxe import calculer_montant
from ..exceptions import SejourNotFoundError

@dataclass
class CalculTaxeResult:
    taxe_id: int
    montant: Decimal

def calculer_taxe_sejour(sejour_id: int, user: User) -> CalculTaxeResult:
    """Calculate tax for a stay - main use case."""
    sejour = Sejour.objects.select_related("logement").get(pk=sejour_id)
    
    # Permission check
    if not can_calculer_taxe(user, sejour):
        raise PermissionDenied("Cannot calculate tax")
    
    with transaction.atomic():
        montant = calculer_montant(sejour)
        taxe = TaxeSejour.objects.create(
            sejour=sejour,
            montant=montant,
            created_by=user,
        )
    
    return CalculTaxeResult(taxe_id=taxe.id, montant=montant)
```

### 2. Domain Services (Business Rules)

Pure logic, no I/O:

```python
# apps/taxe_sejour/services/domain/regles_taxe.py
from decimal import Decimal

def calculer_montant(sejour: Sejour) -> Decimal:
    """Pure business rule - no database, no HTTP."""
    nb_nuits = (sejour.date_fin - sejour.date_debut).days
    taux = sejour.logement.categorie.taux_taxe
    return Decimal(nb_nuits * sejour.nb_personnes) * taux

def valider_periode(date_debut: date, date_fin: date) -> bool:
    """Validation rule."""
    return date_fin >= date_debut
```

### 3. Integration Services

Encapsulate ALL external interactions:

```python
# apps/taxe_sejour/services/integrations/erp_bridge.py
import requests

class ERPBridge:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def fetch_taux_taxe(self, commune_code: str, date: date) -> Decimal:
        """Fetch tax rate from ERP - encapsulates HTTP details."""
        response = requests.get(
            f"{self.base_url}/taux",
            params={"commune": commune_code, "date": date.isoformat()},
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return Decimal(response.json()["taux"])
```

### 4. ETL Services

```python
# apps/labo/services/etl/extract_xlsx.py
def extract_fichier_xlsx(file_path: str) -> list[dict]:
    """Extract raw data from Excel file."""
    ...

# apps/labo/services/etl/transform_data.py  
def transform_donnees(raw_data: list[dict]) -> list[LaboDataDTO]:
    """Clean, validate, map to DTOs."""
    ...

# apps/labo/services/etl/load_data.py
def load_donnees(data: list[LaboDataDTO]) -> int:
    """Bulk create/update models."""
    Analyse.objects.bulk_create([...], batch_size=1000)
    return len(data)
```

## Calling Services

### From Views

```python
# apps/taxe_sejour/views/backoffice.py
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from ..services.usecases.calculer_taxe import calculer_taxe_sejour

class CalculerTaxeView(LoginRequiredMixin, View):
    def post(self, request, sejour_id):
        result = calculer_taxe_sejour(
            sejour_id=sejour_id,
            user=request.user
        )
        return redirect("taxe_sejour:detail", pk=result.taxe_id)
```

### From DRF ViewSets

```python
# apps/taxe_sejour/api/viewsets/taxe.py
class TaxeViewSet(viewsets.GenericViewSet):
    def create(self, request):
        result = calculer_taxe_sejour(
            sejour_id=request.data["sejour_id"],
            user=request.user,
        )
        return Response({"taxe_id": result.taxe_id}, status=201)
```

### From Management Commands

```python
# apps/taxe_sejour/management/commands/recalc_taxe.py
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--periode", required=True)
    
    def handle(self, *args, **options):
        count = recalculer_taxes(periode=options["periode"])
        self.stdout.write(f"{count} taxes recalculated")
```

## DTOs and Exceptions

```python
# apps/taxe_sejour/services/dto.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class TaxeCalculeeDTO:
    taxe_id: int
    montant: Decimal
    periode: str

# apps/taxe_sejour/exceptions.py
class TaxeError(Exception):
    """Base exception for taxe domain."""
    pass

class SejourNotFoundError(TaxeError):
    pass

class TaxeDejaCalculeeError(TaxeError):
    pass
```

## Permissions

```python
# apps/taxe_sejour/permissions.py
def can_calculer_taxe(user: User, sejour: Sejour) -> bool:
    if user.is_superuser:
        return True
    return (
        user.has_perm("taxe_sejour.add_taxesejour")
        and sejour.commune in user.communes.all()
    )

# Usage in service
from .permissions import can_calculer_taxe

def calculer_taxe_sejour(sejour_id: int, user: User):
    sejour = Sejour.objects.get(pk=sejour_id)
    if not can_calculer_taxe(user, sejour):
        raise PermissionDenied("Not authorized")
    ...
```

## DO ✅

```python
# ✅ Transactions at use case level
def create_sejour_and_taxe(data, user):
    with transaction.atomic():
        sejour = Sejour.objects.create(...)
        taxe = calculate_taxe(sejour)
        return taxe

# ✅ Dependency injection via arguments
def calculer_taxe(sejour_id, user, taxe_repo=None):
    taxe_repo = taxe_repo or TaxeSejour.objects
    ...

# ✅ Services return DTOs or models, not HTTP responses
def process_import(file) -> ImportResultDTO:
    ...
    return ImportResultDTO(count=100, errors=[])

# ✅ Use cases accept user for security
def delete_sejour(sejour_id: int, user: User):
    ...
```

## DON'T ❌

```python
# ❌ Business logic in views
class TaxeView(View):
    def post(self, request):
        montant = request.POST["nuits"] * request.POST["taux"]  # BAD

# ❌ Business logic in serializers
class TaxeSerializer(serializers.Serializer):
    def create(self, validated_data):
        montant = self.calculate_complex_tax()  # BAD

# ❌ Services returning HTTP responses
def calculer_taxe(sejour_id):
    ...
    return HttpResponse(...)  # BAD

# ❌ Services accessing request directly
def process(request):  # BAD - accept only needed params
    user = request.user
    ...

# ❌ HTTP calls in use cases (should be in integrations/)
def calculer_taxe(sejour_id):
    response = requests.get(...)  # BAD - use integration service

# ❌ Heavy logic in signals
@receiver(post_save, sender=Sejour)
def on_save(sender, instance, **kwargs):
    recalculate_all_taxes(instance)  # BAD

# ❌ Service layer for trivial CRUD
class CreateUserService:  # Over-engineering for simple CRUD
    def execute(self, data):
        return User.objects.create(**data)
```

## Signals - Limited Use

```python
# ✅ OK for signals: lightweight side-effects
@receiver(post_save, sender=Sejour)
def log_sejour_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Sejour {instance.id} created")
        metrics.increment("sejour.created")

# ❌ NOT OK: main business logic
@receiver(post_save, sender=Sejour)
def calculate_everything(sender, instance, **kwargs):
    recalc_taxe(instance)       # BAD
    notify_comptabilite(instance)  # BAD
    update_reporting(instance)  # BAD
```

## Checklist

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
