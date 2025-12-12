# Django Performance & Scalability Rules

## Performance Categories

1. **Interactive Performance**: View/API latency, user experience
2. **Batch Performance**: ETL processing time, report generation
3. **Scalability**: Handling more users, data, load

## ORM Optimization

### N+1 Query Prevention

```python
# ❌ BAD: N+1 queries
orders = Order.objects.all()
for order in orders:
    print(order.customer.name)  # Query per order!

# ✅ GOOD: Single query with JOIN
orders = Order.objects.select_related("customer").all()
for order in orders:
    print(order.customer.name)  # No additional query
```

### select_related vs prefetch_related

```python
# select_related: ForeignKey, OneToOne (SQL JOIN)
Order.objects.select_related("customer", "shipping_address")

# prefetch_related: ManyToMany, reverse FK (separate query + Python join)
Order.objects.prefetch_related("items", "items__product")

# Combined
Order.objects.select_related("customer").prefetch_related("items__product")
```

### ViewSet with Optimized Queryset
```python
class OrderViewSet(ModelViewSet):
    queryset = (
        Order.objects
        .select_related("customer", "shipping_address")
        .prefetch_related(
            "items",
            "items__product",
            "items__product__category",
        )
    )
    serializer_class = OrderSerializer
```

### Limit Fields with only/defer

```python
# Only fetch needed fields
Order.objects.only("id", "status", "total", "created_at")

# Exclude heavy fields
Order.objects.defer("notes", "internal_comments")
```

## Database Indexing

### Model Index Definition
```python
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            # Single column
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            # Composite (for common filter combinations)
            models.Index(fields=["customer", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]
```

### PostgreSQL-Specific Indexes
```python
from django.contrib.postgres.indexes import GinIndex, BTreeIndex

class Product(models.Model):
    name = models.CharField(max_length=200)
    tags = models.JSONField(default=list)
    search_vector = SearchVectorField(null=True)
    
    class Meta:
        indexes = [
            # GIN for JSONB/Array/Full-text
            GinIndex(fields=["tags"]),
            GinIndex(fields=["search_vector"]),
            # Partial index
            models.Index(
                fields=["status"],
                name="active_orders_idx",
                condition=Q(status="active"),
            ),
        ]
```

## API Performance

### Mandatory Pagination
```python
# config/settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,  # Reasonable default
}

# For large datasets, use cursor pagination
from rest_framework.pagination import CursorPagination

class LogPagination(CursorPagination):
    page_size = 100
    ordering = "-created_at"

class LogViewSet(ReadOnlyModelViewSet):
    pagination_class = LogPagination
```

### Explicit Filter/Ordering Fields
```python
class OrderViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "customer"]
    search_fields = ["customer__name", "reference"]
    
    # Whitelist ordering fields (must have indexes!)
    ordering_fields = ["created_at", "total"]  # Not "__all__"
    ordering = ["-created_at"]
```

### Avoid Heavy Serializer Computations
```python
# ❌ BAD: Computation per object
class OrderSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()
    
    def get_item_count(self, obj):
        return obj.items.count()  # Query per object!

# ✅ GOOD: Use annotation
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.annotate(
        item_count=Count("items")
    )

class OrderSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(read_only=True)
```

## Caching

### Cache Configuration
```python
# config/settings/base.py
CACHES = {
    "default": env.cache("CACHE_URL", default="locmem://"),
}

# Production: Redis
# CACHE_URL=redis://redis:6379/1
```

### Service-Level Caching
```python
from django.core.cache import cache

def get_tax_parameters(region_id: int):
    cache_key = f"tax_params:{region_id}"
    params = cache.get(cache_key)
    
    if params is None:
        params = TaxParameter.objects.get(region_id=region_id)
        cache.set(cache_key, params, timeout=300)  # 5 minutes
    
    return params

def invalidate_tax_parameters(region_id: int):
    cache.delete(f"tax_params:{region_id}")
```

### View-Level Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def public_stats_view(request):
    # Expensive computation
    return render(request, "stats.html", context)
```

## Bulk Operations

### Bulk Create
```python
# ❌ BAD: Individual saves
for data in records:
    Record.objects.create(**data)

# ✅ GOOD: Bulk create
Record.objects.bulk_create([
    Record(**data) for data in records
], batch_size=1000)
```

### Bulk Update
```python
# Update many records efficiently
Record.objects.filter(status="pending").update(
    status="processed",
    processed_at=timezone.now(),
)

# Or with bulk_update for different values
records = list(Record.objects.filter(status="pending"))
for record in records:
    record.status = "processed"
Record.objects.bulk_update(records, ["status"], batch_size=1000)
```

### Upsert Pattern (PostgreSQL)
```python
from django.db.models import F

# Using update_or_create
for data in records:
    Record.objects.update_or_create(
        external_id=data["id"],  # Lookup key
        defaults={
            "name": data["name"],
            "value": data["value"],
        },
    )
```

## ETL Performance

### Chunked Processing
```python
def process_large_file(file_path: Path, chunk_size: int = 1000):
    import pandas as pd
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        records = [transform_row(row) for _, row in chunk.iterrows()]
        Record.objects.bulk_create(records, ignore_conflicts=True)
        
        logger.info(f"Processed {len(records)} records")
```

### Transaction Batching
```python
from django.db import transaction

def import_records(records: list[dict], batch_size: int = 500):
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        with transaction.atomic():
            for record_data in batch:
                process_record(record_data)
        
        logger.info(f"Committed batch {i // batch_size + 1}")
```

## Scalability Patterns

### Stateless Application
```python
# Sessions: Use DB or Redis (not memory)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"  # Redis

# File uploads: Use shared storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# Or shared volume in Docker
```

### Celery Queue Separation
```python
# config/celery.py
app.conf.task_routes = {
    "apps.*.tasks.etl_*": {"queue": "etl"},
    "apps.*.tasks.notification_*": {"queue": "notifications"},
    "apps.*.tasks.*": {"queue": "default"},
}

# docker-compose.yml
services:
  worker_default:
    command: celery -A config worker -Q default -c 4
  worker_etl:
    command: celery -A config worker -Q etl -c 2
```

## Monitoring Queries

### Debug Toolbar (Development)
```python
# config/settings/dev.py
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
```

### Query Logging
```python
# Temporary debugging
import logging
logging.getLogger("django.db.backends").setLevel(logging.DEBUG)
```

### Analyze Slow Queries
```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

---

## ✅ DO

- ✅ Use `select_related`/`prefetch_related` in list views
- ✅ Index fields used in filters and ordering
- ✅ Paginate all list endpoints (reasonable page size)
- ✅ Whitelist `ordering_fields` explicitly
- ✅ Use `annotate` instead of SerializerMethodField for counts
- ✅ Cache frequently-accessed reference data
- ✅ Use bulk operations for ETL (bulk_create, bulk_update)
- ✅ Process large files in chunks
- ✅ Keep application stateless (sessions in cache/DB)
- ✅ Separate Celery queues by task type

---

## ❌ DON'T

- ❌ **No N+1 queries** - always optimize relations
- ❌ **No unlimited list responses** - always paginate
- ❌ **No ordering on non-indexed fields** in production
- ❌ **No heavy computation in serializers** - use annotations
- ❌ **No long-running transactions** - batch and commit
- ❌ **No synchronous heavy processing** in HTTP thread
- ❌ **No in-memory sessions** - breaks horizontal scaling

---

## Performance Checklist

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
