# Django Models & ORM Reference

## Base Model Pattern

```python
# shared/models.py
from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    """Abstract base model with audit timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SoftDeleteModel(TimeStampedModel):
    """Abstract model with soft delete support."""

    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

## Model Definition Best Practices

```python
# apps/production/models/lot.py
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from shared.models import TimeStampedModel

class Lot(TimeStampedModel):
    """Production lot with quality tracking."""

    # Explicit field definitions
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code lot",
        help_text="Identifiant unique du lot"
    )

    # FK with explicit on_delete and related_name
    campagne = models.ForeignKey(
        'production.Campagne',
        on_delete=models.PROTECT,  # Prevent accidental deletion
        related_name='lots',
        db_index=True,  # Explicit index for filtered queries
    )

    operateur = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='lots_produits',
    )

    # DecimalField for precision (never FloatField for money/quantities)
    quantite = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )

    # Status with choices
    STATUS_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('VALIDE', 'Validé'),
        ('ARCHIVE', 'Archivé'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='BROUILLON',
        db_index=True,
    )

    class Meta:
        db_table = 'production_lots'
        ordering = ['-created_at']
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'

        # Database-level constraints
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantite__gt=0),
                name='lot_quantite_positive'
            ),
        ]

        # Composite indexes for common queries
        indexes = [
            models.Index(fields=['campagne', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return f"{self.code} ({self.status})"

    # Properties for computed values
    @property
    def est_conforme(self) -> bool:
        """Check if lot passes all quality controls."""
        return self.analyses.filter(conforme=False).count() == 0
```

## Custom QuerySet & Manager

```python
# apps/production/models/lot.py (continued)

class LotQuerySet(models.QuerySet):
    """Custom QuerySet with domain-specific filters."""

    def actifs(self):
        """Filter active (non-archived) lots."""
        return self.exclude(status='ARCHIVE')

    def par_campagne(self, campagne_id: int):
        """Filter by campaign."""
        return self.filter(campagne_id=campagne_id)

    def avec_analyses(self):
        """Prefetch related analyses (avoid N+1)."""
        return self.prefetch_related('analyses')

    def avec_relations(self):
        """Load all FK relations (avoid N+1)."""
        return self.select_related('campagne', 'operateur')\
                   .prefetch_related('analyses')

    def total_quantite(self) -> Decimal:
        """Aggregate total quantity."""
        from django.db.models import Sum
        result = self.aggregate(total=Sum('quantite'))
        return result['total'] or Decimal('0')

class LotManager(models.Manager):
    """Custom manager using LotQuerySet."""

    def get_queryset(self) -> LotQuerySet:
        return LotQuerySet(self.model, using=self._db)

    def actifs(self):
        return self.get_queryset().actifs()

    def avec_relations(self):
        return self.get_queryset().avec_relations()

# Add to model
class Lot(TimeStampedModel):
    # ... fields ...

    objects = LotManager()
```

## N+1 Query Prevention

### The Problem

```python
# BAD - N+1 queries (1 + N database hits)
lots = Lot.objects.all()
for lot in lots:
    print(lot.campagne.nom)     # 1 query per lot!
    print(lot.operateur.email)  # 1 query per lot!
```

### The Solution

```python
# GOOD - select_related for ForeignKey/OneToOne (SQL JOIN)
lots = Lot.objects.select_related('campagne', 'operateur').all()
for lot in lots:
    print(lot.campagne.nom)     # No extra query
    print(lot.operateur.email)  # No extra query

# GOOD - prefetch_related for ManyToMany/Reverse FK (2 queries total)
campagnes = Campagne.objects.prefetch_related('lots').all()
for campagne in campagnes:
    for lot in campagne.lots.all():  # No extra query
        print(lot.code)

# ADVANCED - Prefetch with custom queryset
from django.db.models import Prefetch

campagnes = Campagne.objects.prefetch_related(
    Prefetch(
        'lots',
        queryset=Lot.objects.filter(status='VALIDE').order_by('-created_at')
    )
).all()
```

### ViewSet Integration

```python
# apps/production/api/viewsets.py
class LotViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        # ALWAYS optimize queries in get_queryset
        return Lot.objects.select_related('campagne', 'operateur')\
                          .prefetch_related('analyses')
```

## Bulk Operations

```python
# apps/production/services/etl/import_lots.py

def import_lots_from_csv(filepath: str, campagne_id: int) -> int:
    """Bulk import lots from CSV file."""
    import csv

    lots_to_create = []

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lots_to_create.append(
                Lot(
                    code=row['code'],
                    quantite=Decimal(row['quantite']),
                    campagne_id=campagne_id,
                    status='BROUILLON',
                )
            )

    # Single INSERT with many rows
    created = Lot.objects.bulk_create(
        lots_to_create,
        batch_size=1000,
        ignore_conflicts=True,  # Skip duplicates
    )

    return len(created)

def update_lots_status(lot_ids: list, new_status: str) -> int:
    """Bulk update lot statuses."""
    return Lot.objects.filter(id__in=lot_ids).update(
        status=new_status,
        updated_at=timezone.now(),
    )
```

## Database Constraints

```python
class Lot(models.Model):
    class Meta:
        constraints = [
            # Check constraint (database-level validation)
            models.CheckConstraint(
                check=models.Q(quantite__gt=0),
                name='lot_quantite_positive'
            ),

            # Unique constraint
            models.UniqueConstraint(
                fields=['campagne', 'code'],
                name='unique_lot_per_campagne'
            ),

            # Conditional unique constraint
            models.UniqueConstraint(
                fields=['code'],
                condition=models.Q(status='ACTIF'),
                name='unique_active_lot_code'
            ),
        ]
```

## Signals (Use Sparingly)

```python
# apps/production/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Lot)
def on_lot_created(sender, instance, created, **kwargs):
    """
    Lightweight side-effect only.
    For heavy operations, use Celery tasks.
    """
    if created:
        # OK: Lightweight logging
        logger.info(f"Lot {instance.code} created")

        # BAD: Heavy operations - use Celery instead
        # send_notification_email(instance)  # NO!
```

## Model Validation

```python
class Lot(models.Model):

    def clean(self):
        """Model-level validation (called by full_clean)."""
        from django.core.exceptions import ValidationError

        # Cross-field validation
        if self.status == 'VALIDE' and self.quantite <= 0:
            raise ValidationError({
                'quantite': 'Validated lots must have positive quantity'
            })

        # Business rule validation
        if self.campagne.status == 'TERMINE':
            raise ValidationError(
                'Cannot modify lots in closed campaigns'
            )

    def save(self, *args, **kwargs):
        # Do NOT put heavy logic here
        # Only call clean() if needed
        self.full_clean()
        super().save(*args, **kwargs)
```

## Annotations & Aggregations

```python
from django.db.models import Count, Sum, Avg, F, Q

# Annotate queryset with computed values
campagnes = Campagne.objects.annotate(
    nombre_lots=Count('lots'),
    quantite_totale=Sum('lots__quantite'),
    taux_conformite=Count('lots', filter=Q(lots__analyses__conforme=True)) * 100.0
                    / Count('lots'),
)

# Use in templates or serializers
for c in campagnes:
    print(f"{c.nom}: {c.nombre_lots} lots, {c.quantite_totale} kg")

# F expressions for database-level operations
Lot.objects.filter(status='BROUILLON').update(
    status='VALIDE',
    quantite=F('quantite') * Decimal('1.05'),  # 5% adjustment
)
```

## Through Models for M2M

```python
# For M2M with audit needs
class Lot(models.Model):
    operateurs = models.ManyToManyField(
        'auth.User',
        through='LotOperateur',
        related_name='lots_assignes',
    )

class LotOperateur(models.Model):
    """Through model with audit fields."""

    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    operateur = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    role = models.CharField(max_length=50)
    assigne_le = models.DateTimeField(auto_now_add=True)
    assigne_par = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignations_faites',
    )

    class Meta:
        unique_together = ['lot', 'operateur']
```
