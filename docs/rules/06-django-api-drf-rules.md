# Django REST Framework API Rules

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Clients                                                │
│  ├── Backoffice (HTML views)                            │
│  ├── React Frontend (API consumer)                      │
│  └── External Systems (ERP, BI, third-party)            │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Django Backend                                         │
│  ├── HTML Views (apps/<app>/views/)                     │
│  └── DRF API (apps/<app>/api/)                          │
│           │                                             │
│           ▼                                             │
│      Services (usecases/, domain/)                      │
│           │                                             │
│           ▼                                             │
│      Models & ORM                                       │
└─────────────────────────────────────────────────────────┘
```

## API Module Structure

```
apps/
  <app_name>/
    api/
      __init__.py
      serializers.py      # DTOs + validation + model mapping
      viewsets.py         # HTTP glue → services
      routers.py          # DRF router registration
      filters.py          # django-filter definitions
      permissions.py      # DRF permission classes
      schemas.py          # (optional) OpenAPI customization
    views/                # HTML views (separate from API)
    services/             # Business logic
    permissions.py        # Domain permission policies (reusable)
```

## URL Configuration

### Root URLs
```python
# config/urls.py
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # HTML routes
    path("items/", include("apps.items.urls")),
    # API routes
    path("api/v1/items/", include("apps.items.api.routers")),
    path("api/v1/orders/", include("apps.orders.api.routers")),
]
```

### App Router
```python
# apps/items/api/routers.py
from rest_framework.routers import DefaultRouter
from .viewsets import ItemViewSet

router = DefaultRouter()
router.register(r"", ItemViewSet, basename="item")

urlpatterns = router.urls
```

## Serializers

### ModelSerializer (CRUD)
```python
# apps/items/api/serializers.py
from rest_framework import serializers
from apps.items.models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "status", "amount", "created_at"]
        read_only_fields = ["id", "created_at"]
```

### Use Case DTOs (Input/Output)
```python
class CalculatePriceInputSerializer(serializers.Serializer):
    item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    force_recalculate = serializers.BooleanField(default=False)

class CalculatePriceOutputSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    breakdown = serializers.DictField()
```

### Nested Serializer
```python
class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ["id", "customer", "items", "total", "status"]
```

## ViewSets

### Standard CRUD ViewSet
```python
# apps/items/api/viewsets.py
from rest_framework import viewsets, permissions
from .serializers import ItemSerializer
from apps.items.models import Item

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.select_related("category")
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
```

### ViewSet with Service Delegation
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.items.services.usecases import calculate_item_price

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=["post"])
    def calculate_price(self, request, pk=None):
        item = self.get_object()
        
        input_serializer = CalculatePriceInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        
        # Delegate to service
        result = calculate_item_price(
            item=item,
            user=request.user,
            **input_serializer.validated_data,
        )
        
        output_serializer = CalculatePriceOutputSerializer(result)
        return Response(output_serializer.data)
```

### APIView for Custom Endpoints
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class WebhookReceiver(APIView):
    permission_classes = []  # Public endpoint
    
    def post(self, request):
        # Validate webhook signature
        # Delegate to service
        return Response({"status": "received"})
```

## Permissions

### DRF Permission Wrapping Domain Policy
```python
# apps/items/api/permissions.py
from rest_framework.permissions import BasePermission
from apps.items.permissions import can_view_item, can_edit_item

class CanViewItemPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return can_view_item(request.user, obj)

class CanEditItemPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return can_edit_item(request.user, obj)
        return True
```

### ViewSet with Multiple Permissions
```python
class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        CanViewItemPermission,
        CanEditItemPermission,
    ]
```

## Filtering, Search & Ordering

### Filter Definition
```python
# apps/items/api/filters.py
import django_filters
from apps.items.models import Item

class ItemFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
    status = django_filters.CharFilter(field_name="status")
    
    class Meta:
        model = Item
        fields = ["status", "category"]
```

### ViewSet with Filters
```python
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ItemFilter

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ItemFilter
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "amount"]  # Explicit whitelist
    ordering = ["-created_at"]  # Default ordering
```

## Pagination Configuration

```python
# config/settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}
```

### Custom Pagination
```python
from rest_framework.pagination import CursorPagination

class LargeResultsCursorPagination(CursorPagination):
    page_size = 100
    ordering = "-created_at"

class LogViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = LargeResultsCursorPagination
```

## Error Handling

### Domain Exception to API Exception
```python
from rest_framework.exceptions import APIException
from apps.items.services.exceptions import ItemInvalidError

class ItemInvalidAPIException(APIException):
    status_code = 400
    default_detail = "Item parameters are invalid."

class ItemViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        try:
            result = process_item(...)
        except ItemInvalidError as exc:
            raise ItemInvalidAPIException(str(exc))
        
        return Response(result)
```

## Global DRF Configuration

```python
# config/settings/base.py
REST_FRAMEWORK = {
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Permissions
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    # Throttling
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}
```

---

## ✅ DO

- ✅ Organize API in `apps/<app>/api/` module
- ✅ Use `ModelSerializer` for standard CRUD
- ✅ Use `Serializer` for use case DTOs (Input/Output pattern)
- ✅ Keep ViewSets thin: delegate to services
- ✅ Use `@action` decorator for custom endpoints
- ✅ Wrap domain permissions in DRF permission classes
- ✅ Explicitly list `ordering_fields` (whitelist)
- ✅ Configure pagination globally
- ✅ Use `select_related`/`prefetch_related` in querysets
- ✅ Map domain exceptions to API exceptions
- ✅ Version API routes: `/api/v1/...`

---

## ❌ DON'T

- ❌ **No business logic in serializers** - validation only
- ❌ **No complex ORM queries in ViewSets** - use services
- ❌ **No transactions in ViewSets** - handle in services
- ❌ **No unlimited ordering** - explicit whitelist required
- ❌ **No pagination on large datasets** - causes timeouts
- ❌ **No public endpoints by default** - require explicit opt-in
- ❌ **No synchronous heavy processing** - use async jobs for ETL
- ❌ **No N+1 queries** - always optimize with select/prefetch

---

## Checklist

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
