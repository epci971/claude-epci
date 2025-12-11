# Django Models & ORM Rules

## Models Package Structure

```
apps/<domain>/
├── models/
│   ├── __init__.py          # Re-export all model classes
│   ├── <model_name>.py      # One file per main model
│   └── mixins.py            # Abstract base classes for this app
```

### Re-export Pattern

```python
# apps/taxe_sejour/models/__init__.py
from .taxe import TaxeSejour
from .parametre import ParametreTaxe
from .mixins import TimeStampedModel
```

## Naming Conventions

- **Class names**: PascalCase singular (`Logement`, `Sejour`, `TaxeSejour`)
- **Field names**: snake_case (`date_debut`, `montant_total`, `is_active`)
- **Related names**: plural snake_case (`sejours`, `logements`)

## Field Types

```python
# Strings - always explicit max_length
nom = models.CharField(max_length=255, verbose_name="Name")

# Money/decimals - use DecimalField, NOT FloatField
montant = models.DecimalField(max_digits=10, decimal_places=2)

# Quantities >= 0
nb_personnes = models.PositiveIntegerField()

# Dates - DateField if time not needed, DateTimeField otherwise
date_debut = models.DateField()
created_at = models.DateTimeField(auto_now_add=True)

# Always add verbose_name and help_text for non-trivial fields
code_insee = models.CharField(
    max_length=5,
    verbose_name="INSEE Code",
    help_text="5-digit French commune identifier"
)
```

## Relations

### ForeignKey Rules

```python
class Sejour(models.Model):
    # Reference data: PROTECT to prevent accidental deletion
    commune = models.ForeignKey(
        "referentiels.Commune",
        on_delete=models.PROTECT,
        related_name="sejours",
    )
    
    # Secondary data: SET_NULL or CASCADE as needed
    import_batch = models.ForeignKey(
        "etl.ImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        related_name="sejours",
    )
```

### ManyToMany - Always Use Through Model

```python
# For audit/traceability, prefer explicit intermediate model
class SejourEquipement(models.Model):
    sejour = models.ForeignKey(Sejour, on_delete=models.CASCADE)
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    date_ajout = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ["sejour", "equipement"]
```

## Constraints & Indexes

```python
class Sejour(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        constraints = [
            # Check constraints for business rules
            models.CheckConstraint(
                check=models.Q(date_fin__gte=models.F("date_debut")),
                name="sejour_date_fin_gte_debut",
            ),
            models.CheckConstraint(
                check=models.Q(montant__gte=0),
                name="sejour_montant_positive",
            ),
            # Unique constraints
            models.UniqueConstraint(
                fields=["logement", "date_debut"],
                name="sejour_unique_logement_date",
            ),
        ]
        indexes = [
            models.Index(fields=["date_debut", "date_fin"]),
            models.Index(fields=["commune", "date_debut"]),
        ]
```

## Abstract Mixins

```python
# shared/models/base.py
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

# Usage: combine mixins
class Sejour(TimeStampedModel, SoftDeleteModel):
    ...
```

## Custom QuerySets & Managers

```python
# apps/sejour/models/sejour.py
class SejourQuerySet(models.QuerySet):
    def actifs(self):
        return self.filter(annule=False, deleted_at__isnull=True)
    
    def avec_logement(self):
        return self.select_related("logement", "commune")
    
    def pour_periode(self, debut, fin):
        return self.filter(date_debut__gte=debut, date_fin__lte=fin)

class Sejour(TimeStampedModel):
    # ... fields ...
    objects = SejourQuerySet.as_manager()

# Usage
Sejour.objects.actifs().avec_logement().pour_periode(d1, d2)
```

## DO ✅

```python
# ✅ select_related for FK/OneToOne (SQL JOIN)
Sejour.objects.select_related("logement", "commune")

# ✅ prefetch_related for M2M/reverse FK (separate query)
Logement.objects.prefetch_related("sejours")

# ✅ bulk operations for ETL
Sejour.objects.bulk_create(sejours_list, batch_size=1000)
Sejour.objects.bulk_update(sejours_list, ["montant", "status"])

# ✅ Indexes on frequently filtered columns
class Meta:
    indexes = [models.Index(fields=["date_debut", "commune"])]
```

## DON'T ❌

```python
# ❌ N+1 queries
for sejour in Sejour.objects.all():
    print(sejour.logement.nom)  # BAD - 1 query per iteration

# ❌ Heavy business logic in models
class Sejour(models.Model):
    def save(self, *args, **kwargs):
        self.recalculate_all_taxes()  # BAD - put in service
        self.send_notification()       # BAD - put in service
        super().save(*args, **kwargs)

# ❌ Network calls in models
class Sejour(models.Model):
    def clean(self):
        response = requests.get(...)  # BAD - never do this

# ❌ ETL in migrations
# BAD - use management commands instead
def migrate_data(apps, schema_editor):
    for item in Model.objects.all():  # BAD for large datasets
        ...

# ❌ FloatField for money
prix = models.FloatField()  # BAD - use DecimalField

# ❌ Missing on_delete
logement = models.ForeignKey(Logement)  # BAD - explicit on_delete

# ❌ Missing related_name
logement = models.ForeignKey(Logement, on_delete=models.PROTECT)  # BAD
```

## Migrations

- **Never modify** committed migrations - create new ones
- **Separate** schema migrations from data migrations
- **Large data operations**: use management commands, NOT migrations
- **Squash** periodically if too many migration files accumulate

## Checklist

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
